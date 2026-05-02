import sqlite3
from datetime import datetime


from database.db import get_db


def _close_db(conn):
    """Helper to close database connection"""
    conn.close()


def get_user_by_id(user_id):
    """Fetch user details by user_id"""
    conn = get_db()
    try:
        result = conn.execute(
            'SELECT id, name, email, created_at FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()
        if result:
            user = dict(result)
            # Format date as "Month YYYY" (e.g., "April 2026")
            # Handle both full datetime (with time) and date-only formats
            created_str = user['created_at']
            if ' ' in created_str:
                # Has timestamp, take only the date part
                created_str = created_str.split(' ')[0]
            created_date = datetime.strptime(created_str, '%Y-%m-%d')
            user['member_since'] = created_date.strftime('%B %Y')
            return user
        return None
    finally:
        _close_db(conn)


def get_summary_stats(user_id, start_date=None, end_date=None):
    """Fetch summary statistics for a user with optional date filtering"""
    conn = get_db()
    try:
        # Get total spent and transaction count with dynamic filtering
        query = '''SELECT SUM(amount) as total_spent, COUNT(*) as transaction_count 
                   FROM expenses 
                   WHERE user_id = ?'''
        params = [user_id]
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
            
        stats = conn.execute(query, params).fetchone()

        result = {
            'total_spent': stats['total_spent'] if stats['total_spent'] else 0.0,
            'transaction_count': stats['transaction_count'] if stats['transaction_count'] else 0,
            'top_category': '—'
        }

        # Get top category if there are transactions
        if result['transaction_count'] > 0:
            top_cat_query = '''SELECT category, SUM(amount) as cat_total
                               FROM expenses
                               WHERE user_id = ?'''
            top_cat_params = [user_id]
            
            if start_date:
                top_cat_query += ' AND date >= ?'
                top_cat_params.append(start_date)
            if end_date:
                top_cat_query += ' AND date <= ?'
                top_cat_params.append(end_date)
                
            top_cat_query += ' GROUP BY category ORDER BY cat_total DESC LIMIT 1'
            
            top_cat = conn.execute(top_cat_query, top_cat_params).fetchone()
            if top_cat:
                result['top_category'] = top_cat['category']

        return result
    finally:
        _close_db(conn)


def get_recent_transactions(user_id, limit=10, start_date=None, end_date=None):
    """Fetch recent transactions for a user with optional date filtering"""
    conn = get_db()
    try:
        query = '''SELECT date, description, category, amount
                FROM expenses
                WHERE user_id = ?'''
        params = [user_id]
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
            
        query += ' ORDER BY date DESC LIMIT ?'
        params.append(limit)
        
        rows = conn.execute(query, params).fetchall()

        return [dict(row) for row in rows]
    finally:
        _close_db(conn)


def get_category_breakdown(user_id, start_date=None, end_date=None):
    """Fetch category breakdown with percentages and optional date filtering"""
    conn = get_db()
    try:
        # Get totals per category with dynamic filtering
        query = '''SELECT category, SUM(amount) as total
                FROM expenses
                WHERE user_id = ?'''
        params = [user_id]
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
            
        query += ' GROUP BY category ORDER BY total DESC'
        
        rows = conn.execute(query, params).fetchall()

        if not rows:
            return []

        # Convert to list of dicts and calculate percentages
        breakdown = []
        total_sum = sum(row['total'] for row in rows)

        for row in rows:
            pct = round((row['total'] / total_sum) * 100) if total_sum > 0 else 0
            breakdown.append({
                'name': row['category'],
                'total': f"₹{row['total']:.2f}",
                'percentage': pct
            })

        # Adjust for rounding to ensure percentages sum to 100
        if breakdown:
            total_pct = sum(item['percentage'] for item in breakdown)
            if total_pct != 100:
                # Adjust the largest category to absorb the rounding difference
                max_idx = 0
                max_pct = breakdown[0]['percentage']
                for i, item in enumerate(breakdown):
                    if item['percentage'] > max_pct:
                        max_pct = item['percentage']
                        max_idx = i
                breakdown[max_idx]['percentage'] += (100 - total_pct)

        return breakdown
    finally:
        _close_db(conn)