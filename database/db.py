import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


def is_valid_email(email):
    """
    Validates email format
    Returns True if email contains @ and . after @
    """
    email = email.strip()
    if not email or '@' not in email:
        return False
    
    local, domain = email.rsplit('@', 1)
    return bool(local) and '.' in domain


def is_valid_password(password):
    """
    Validates password length (minimum 8 characters)
    Returns True if password is valid
    """
    return bool(password and len(password) >= 8)


def email_exists(email):
    """
    Checks if email already exists in users table
    Returns True if email found, False otherwise
    """
    db = get_db()
    result = db.execute('SELECT COUNT(*) FROM users WHERE email = ?', (email.strip(),)).fetchone()
    db.close()
    return result[0] > 0


def create_user(email, password, name):
    """
    Creates a new user with email, password, and name
    Hashes password using werkzeug
    Returns user_id on success
    Raises ValueError on validation error or duplicate email
    """
    # Strip whitespace
    email = email.strip()
    password = password.strip()
    name = name.strip()
    
    # Validate name
    if not name:
        raise ValueError("Full name is required")
    
    # Validate email
    if not email:
        raise ValueError("Email is required")
    
    if not is_valid_email(email):
        raise ValueError("Please enter a valid email address")
    
    # Check for duplicate email
    if email_exists(email):
        raise ValueError("Email already registered. Try logging in instead.")
    
    # Validate password
    if not password:
        raise ValueError("Password is required")
    
    if not is_valid_password(password):
        raise ValueError("Password must be at least 8 characters")
    
    # Hash password
    password_hash = generate_password_hash(password)
    
    # Create user in database
    db = get_db()
    try:
        db.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, password_hash)
        )
        db.commit()
        user_id = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()[0]
        db.close()
        return user_id
    except sqlite3.IntegrityError:
        db.close()
        raise ValueError("Email already registered. Try logging in instead.")


def get_user_by_email(email):
    """
    Queries user by email from database
    Returns user dict (id, name, email, password_hash) or None if not found
    """
    email = email.strip()
    db = get_db()
    result = db.execute('SELECT id, name, email, password_hash FROM users WHERE email = ?', (email,)).fetchone()
    db.close()
    return dict(result) if result else None


def get_user_by_id(user_id):
    """
    Queries user by user_id from database
    Returns user dict (id, name, email) or None if not found
    """
    db = get_db()
    result = db.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,)).fetchone()
    db.close()
    return dict(result) if result else None


def validate_user(email, password):
    """
    Validates email and password against database
    Returns user_id on success, None on failure
    """
    email = email.strip()
    user = get_user_by_email(email)
    
    if user and check_password_hash(user['password_hash'], password):
        return user['id']
    
    return None


def get_db():
    """
    Opens connection to Finlo.db in project root
    - Sets row_factory for dictionary-like access
    - Enables foreign key constraints
    Returns the connection
    """
    conn = sqlite3.connect('Finlo.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


def init_db():
    """
    Creates both tables using CREATE TABLE IF NOT EXISTS
    Safe to call multiple times
    """
    db = get_db()
    
    # Create users table
    sql_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
    
    # Create expenses table
    sql_expenses = "CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, amount REAL NOT NULL, category TEXT NOT NULL, date TEXT NOT NULL, description TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))"
    
    db.execute(sql_users)
    db.execute(sql_expenses)
    
    db.commit()
    db.close()


def seed_db(): 
    """
    Inserts demo data:
    - One demo user with hashed password
    - 8 sample expenses across all categories
    Prevents duplicate inserts on multiple runs
    """
    db = get_db()
    
    # Check if data already exists
    existing_user = db.execute('SELECT email FROM users WHERE email = ?', ('demo@Finlo.com',)).fetchone()
    
    if not existing_user:
        # Insert demo user with hashed password
        hash_password = generate_password_hash('demo123')
        db.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            ('Demo User', 'demo@Finlo.com', hash_password)
        )
        
        # Get the user ID we just created (for FK validation)
        user_id = db.execute('SELECT id FROM users WHERE email = ?', ('demo@Finlo.com',)).fetchone()[0]
        
        # Insert 8 sample expenses covering all 7 categories
        # Note: We have 8 expenses for 7 categories, so one category appears twice
        # This ensures we meet both requirements: "8 sample expenses" + "at least one per category"
        categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Shopping', 'Other', 'Transport']
        
        for i, category in enumerate(categories):
            # Generate dates starting from the 1st of the current month
            # This safely handles month boundaries without overflow
            current_month_start = datetime.now().replace(day=1)
            expense_date = (current_month_start + timedelta(days=i)).strftime('%Y-%m-%d')
            
            db.execute(
                'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                (user_id, 10.0 + i * 5.0, category, expense_date, f'Sample {category} expense')
            )
        
        db.commit()
    
    db.close()
