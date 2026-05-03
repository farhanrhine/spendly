import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from database.db import get_db, init_db, seed_db, create_user, validate_user, get_user_by_id
from database.queries import get_user_by_id as get_user_details, get_summary_stats, get_recent_transactions, get_category_breakdown, create_expense

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')


# Initialize database on startup
with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    user = None
    if session.get('user_id'):
        user = get_user_by_id(session['user_id'])
    return render_template("landing.html", user=user)


@app.route("/register")
def register():
    # Redirect already logged-in users away from register page
    if session.get('user_id'):
        return redirect(url_for('landing'))
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    """
    Handles registration form submission
    Validates email, password, and confirm password, creates user, sets session, redirects to landing
    """
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    name = request.form.get('name', '').strip()
    
    # Validate confirm password matches
    if password != confirm_password:
        return render_template("register.html", error="Passwords do not match")
    
    try:
        user_id = create_user(email, password, name)
        session['user_id'] = user_id
        return redirect(url_for('landing'))
    except ValueError as e:
        return render_template("register.html", error=str(e))


@app.route("/login")
def login():
    # Redirect already logged-in users away from login page
    if session.get('user_id'):
        return redirect(url_for('landing'))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    """
    Handles login form submission
    Validates email and password, sets session, redirects to landing
    """
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    user_id = validate_user(email, password)
    
    if user_id:
        session['user_id'] = user_id
        return redirect(url_for('landing'))
    else:
        return render_template("login.html", error="Invalid email or password")


@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")

# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout", methods=["POST"])
def logout():
    """
    Handles logout — clears session and redirects to landing page
    """
    session.clear()
    return redirect(url_for('landing'))


@app.route("/profile")
def profile():
    """
    Displays user profile page with dynamic data from database.
    Only accessible to authenticated users.
    """
    # Authentication guard
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    from datetime import timedelta
    
    # Get date filters from query parameters
    range_type = request.args.get('range')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    today = datetime.now()
    active_range = range_type or 'custom'
    
    # Handle Quick Filters
    if range_type == 'this_month':
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    elif range_type == 'last_month':
        last_month_end = today.replace(day=1) - timedelta(days=1)
        start_date = last_month_end.replace(day=1).strftime('%Y-%m-%d')
        end_date = last_month_end.strftime('%Y-%m-%d')
    elif range_type == 'last_3_months':
        start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
    elif range_type == 'all':
        start_date = None
        end_date = None
    elif start_date or end_date:
        active_range = 'custom'

    # Validate dates (Security Review suggestion)
    def validate_date(date_str):
        if not date_str: return None
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except (ValueError, TypeError):
            return None

    valid_start = validate_date(start_date)
    valid_end = validate_date(end_date)
    
    # Fetch dynamic data from database
    user = get_user_details(user_id)
    if not user:
        return redirect(url_for('login'))
    
    # Add initials
    user['initials'] = ''.join(word[0].upper() for word in user['name'].split())
    
    # Fetch stats with validated filters
    raw_stats = get_summary_stats(user_id, start_date=valid_start, end_date=valid_end)
    
    # Format stats for display (Quality Review suggestion: cleaner data mapping)
    stats = {
        'total_spent': f"₹{raw_stats['total_spent']:.2f}" if raw_stats['total_spent'] > 0 else "₹0.00",
        'transaction_count': raw_stats['transaction_count'],
        'top_category': raw_stats['top_category'] if raw_stats['top_category'] != '—' else "None"
    }
    
    # Fetch transactions and format amounts
    transactions = get_recent_transactions(user_id, limit=10, start_date=valid_start, end_date=valid_end)
    for txn in transactions:
        txn['amount'] = f"₹{txn['amount']:.2f}"
    
    # Fetch category breakdown
    categories = get_category_breakdown(user_id, start_date=valid_start, end_date=valid_end)
    
    context = {
        'user': user,
        'stats': stats,
        'transactions': transactions,
        'categories': categories,
        'start_date': valid_start,
        'end_date': valid_end,
        'active_range': active_range
    }
    
    return render_template('profile.html', **context)


@app.route("/analytics")
def analytics():
    """
    Displays the analytics coming soon page.
    Only accessible to authenticated users.
    """
    # Authentication guard
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    return render_template("analytics.html")


@app.route("/expenses/add")
def add_expense():
    """
    Display the expense entry form.
    Only accessible to authenticated users.
    """
    # Authentication guard
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    # Generate CSRF token if not already in session
    import secrets
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    csrf_token = session.get('csrf_token')
    
    # Categories list
    categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
    default_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('add_expense.html', categories=categories, default_date=default_date, csrf_token=csrf_token)


@app.route("/expenses/add", methods=["POST"])
def add_expense_post():
    """
    Handle expense form submission.
    Validates inputs, creates expense, and redirects to profile.
    """
    # Authentication guard
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    # CSRF token validation
    csrf_token = request.form.get('csrf_token', '')
    session_token = session.get('csrf_token', '')
    if not csrf_token or csrf_token != session_token:
        categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
        default_date = datetime.now().strftime('%Y-%m-%d')
        return render_template('add_expense.html',
                             categories=categories,
                             default_date=default_date,
                             error='Security token expired. Please refresh and try again.')
    
    # Extract form data
    amount = request.form.get('amount', '').strip()
    category = request.form.get('category', '').strip()
    date = request.form.get('date', '').strip()
    description = request.form.get('description', '').strip()
    
    # Categories list for re-rendering on error
    categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
    default_date = datetime.now().strftime('%Y-%m-%d')
    
    # Validate amount is convertible to float
    try:
        float(amount)
    except ValueError:
        return render_template('add_expense.html',
                             categories=categories,
                             default_date=default_date,
                             error='Amount must be a valid number',
                             amount=amount,
                             category=category,
                             date=date,
                             description=description)
    
    # Try to create the expense
    try:
        expense_id = create_expense(user_id, amount, category, date, description)
        return redirect(url_for('profile'))
    except ValueError as e:
        return render_template('add_expense.html',
                             categories=categories,
                             default_date=default_date,
                             error=str(e),
                             amount=amount,
                             category=category,
                             date=date,
                             description=description)


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
