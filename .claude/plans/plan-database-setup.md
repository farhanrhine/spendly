# Implementation Plan for Database Setup (01-database-setup.md)

## Overview
- Purpose: Implement the database layer as defined in the specification document
- Key components: `get_db()`, `init_db()`, `seed_db()` functions
- Target files: `database/db.py`, `app.py`

## Step-by-Step Implementation

### 1. Database Connection (`get_db()`)
**Location:** `database/db.py`
**Implementation:**
```python
import sqlite3


def get_db():
    # Connect to SQLite database
    conn = sqlite3.connect('Finlo.db')
    # Enable row factory for dictionary access
    conn.row_factory = sqlite3.Row
    # Enable foreign key constraints
    conn.execute('PRAGMA foreign_keys = ON')
    return conn
```

### 2. Schema Initialization (`init_db()`)
**Location:** `database/db.py`
**Implementation:**
```sql
-- User Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT datetime('now')
)

-- Expenses Table
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT datetime('now'),
    FOREIGN KEY(user_id) REFERENCES users(id)
)
```

### 3. Data Seeding (`seed_db()`)
**Location:** `database/db.py`
**Implementation:**
```python
def seed_db():
    db = get_db()
    with db.execute('BEGIN TRANSACTION'):
        # Prevent duplicate users
        if not db.execute('SELECT email FROM users').fetchone():
            # Hash password with werkzeug (requirement from spec)
            from werkzeug.security import generate_password_hash
            hash = generate_password_hash(password='demo123')
            db.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                       ('Demo User', 'demo@Finlo.com', hash))
            
            # Insert 8 sample expenses covering categories
            categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Shopping', 'Other', 'Food']
            from datetime import datetime, timedelta
            
            for i, category in enumerate(categories):
                # Generate date as YYYY-MM-DD (within current month)
                expense_date = (datetime.now().replace(day=1) + timedelta(days=i)).strftime('%Y-%m-%d')
                db.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                           (1, 10.0 + i*5.0, category, expense_date, f'Sample {category} expense'))
    db.commit()
```

## Verification Steps
1. Check database file: `sqlite3 Finlo.db -schema`
2. Validate table schema and constraints
3. Test unique email constraint via duplicate insert attempt
4. Verify foreign key relationships
5. Confirm demo data insertion

## Completion Criteria
- Database initializes without errors on app startup
- All tables and constraints exist
- Demo user exists with hashed password
- 8 sample expenses cover all categories