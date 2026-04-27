#!/usr/bin/env python3
"""
Seed realistic dummy expenses for user_id 3
Generates 30 expenses across 6 months
"""

import sqlite3
from datetime import datetime, timedelta
import random

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('Finlo.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def seed_expenses(user_id, count, months):
    """Generate and insert realistic expenses"""
    
    # Verify user exists
    db = get_db()
    user = db.execute('SELECT id FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        print(f"❌ No user found with id {user_id}.")
        db.close()
        return
    
    db.close()
    
    # Category definitions with realistic descriptions and amounts (in ₹)
    categories = {
        'Food': {
            'descriptions': ['Breakfast', 'Lunch', 'Dinner', 'Grocery shopping', 'Restaurant', 'Coffee', 'Snacks', 'Delivery food'],
            'range': (20, 800),
            'weight': 25
        },
        'Transport': {
            'descriptions': ['Bus ticket', 'Taxi ride', 'Gas fill-up', 'Train ticket', 'Auto rickshaw', 'Parking', 'Bike fuel'],
            'range': (50, 500),
            'weight': 20
        },
        'Bills': {
            'descriptions': ['Electricity bill', 'Water bill', 'Internet bill', 'Phone bill', 'Rent', 'Gas bill'],
            'range': (300, 5000),
            'weight': 15
        },
        'Health': {
            'descriptions': ['Doctor visit', 'Medicine', 'Pharmacy', 'Dental checkup', 'Hospital', 'Gym membership'],
            'range': (100, 2000),
            'weight': 10
        },
        'Entertainment': {
            'descriptions': ['Movie tickets', 'Concert', 'Gaming', 'Music subscription', 'Streaming', 'Book'],
            'range': (300, 1500),
            'weight': 10
        },
        'Shopping': {
            'descriptions': ['Clothing', 'Shoes', 'Electronics', 'Home items', 'Fashion', 'Accessories'],
            'range': (400, 5000),
            'weight': 15
        },
        'Other': {
            'descriptions': ['Miscellaneous', 'Gift', 'Tips', 'Subscription', 'Services', 'Personal care'],
            'range': (10, 1000),
            'weight': 5
        }
    }
    
    # Calculate weighted category distribution
    categories_list = []
    for cat, data in categories.items():
        categories_list.extend([cat] * data['weight'])
    
    # Generate expenses across past months
    expenses = []
    now = datetime.now()
    
    for i in range(count):
        # Random date within the past N months
        days_back = random.randint(0, months * 30)
        expense_date = (now - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        # Pick category based on weighted distribution
        category = random.choice(categories_list)
        cat_data = categories[category]
        
        # Generate amount
        amount = round(random.uniform(cat_data['range'][0], cat_data['range'][1]), 2)
        
        # Generate description
        description = random.choice(cat_data['descriptions'])
        
        expenses.append({
            'user_id': user_id,
            'category': category,
            'description': description,
            'amount': amount,
            'date': expense_date
        })
    
    # Insert all expenses in a transaction
    db = get_db()
    try:
        for exp in expenses:
            db.execute(
                'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                (exp['user_id'], exp['amount'], exp['category'], exp['date'], exp['description'])
            )
        db.commit()
        print(f"✅ Successfully inserted {count} expenses for user_id {user_id}")
        
        # Get date range
        dates = [e['date'] for e in expenses]
        print(f"📅 Date range: {min(dates)} to {max(dates)}")
        
        # Show sample of 5 expenses
        print("\n📋 Sample of inserted expenses:")
        print(f"{'Date':<12} {'Category':<15} {'Description':<20} {'Amount':<10}")
        print("-" * 60)
        for exp in random.sample(expenses, min(5, len(expenses))):
            print(f"{exp['date']:<12} {exp['category']:<15} {exp['description']:<20} ₹{exp['amount']:<9.2f}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting expenses: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    user_id = 3
    count = 30
    months = 6
    
    print(f"🌱 Seeding {count} expenses for user_id {user_id} across {months} months...\n")
    seed_expenses(user_id, count, months)
