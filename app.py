from flask import Flask, render_template, request, redirect, url_for, session
from database.db import get_db, init_db, seed_db, create_user, validate_user, get_user_by_id

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'


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
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
