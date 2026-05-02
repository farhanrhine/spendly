import pytest
from app import app as flask_app
from database.db import init_db, create_user, get_db
from flask import url_for

import os
import tempfile
from datetime import datetime, timedelta

@pytest.fixture
def app():
    """Flask app with test config."""
    db_fd, db_path = tempfile.mkstemp()
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test-secret-key',
        'SERVER_NAME': 'localhost.localdomain' # Required for url_for in tests
    })
    with flask_app.app_context():
        init_db()
        yield flask_app
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()

@pytest.fixture
def auth_client(client, app):
    """Test client already logged in with demo user."""
    with app.app_context():
        # Create a user directly in the test DB
        user_id = create_user('test@example.com', 'password123', 'Test User')
        
        # Manually seed some expenses for this user
        db = get_db()
        expenses = [
            (user_id, 100.0, 'Food', '2026-04-01', 'Lunch'),
            (user_id, 200.0, 'Transport', '2026-04-10', 'Bus'),
            (user_id, 300.0, 'Bills', '2026-04-20', 'Rent'),
        ]
        for exp in expenses:
            db.execute(
                'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                exp
            )
        db.commit()
        db.close()

    # Login
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    return client

def test_profile_auth_guard(client):
    """Unauthenticated access to profile should redirect to login."""
    response = client.get('/profile')
    assert response.status_code == 302
    assert '/login' in response.location

def test_profile_filter_presence(auth_client):
    """Profile page should contain the filter form."""
    response = auth_client.get('/profile')
    assert response.status_code == 200
    assert b'START DATE' in response.data.upper()
    assert b'END DATE' in response.data.upper()
    assert b'Apply' in response.data
    assert b'Clear' in response.data
    assert b'This Month' in response.data

def test_profile_filter_persistence(auth_client):
    """Selected dates should persist in the form after filtering."""
    start_date = '2026-04-01'
    end_date = '2026-04-15'
    response = auth_client.get(f'/profile?start_date={start_date}&end_date={end_date}')
    assert response.status_code == 200
    assert f'value="{start_date}"'.encode() in response.data
    assert f'value="{end_date}"'.encode() in response.data

def test_profile_filter_data_restriction(auth_client):
    """Data should be restricted by the selected date range."""
    # All-time data (should have 3 transactions, total 600)
    response_all = auth_client.get('/profile')
    assert b'3' in response_all.data # Transaction count
    assert b'600.00' in response_all.data # Total spent
    
    # Filtered data (only 2026-04-01 to 2026-04-15: Lunch and Bus, total 300)
    response_filtered = auth_client.get('/profile?start_date=2026-04-01&end_date=2026-04-15')
    assert b'2' in response_filtered.data # Transaction count
    assert b'300.00' in response_filtered.data # Total spent
    assert b'Lunch' in response_filtered.data
    assert b'Bus' in response_filtered.data
    assert b'Rent' not in response_filtered.data

def test_profile_filter_clear(auth_client):
    """Clicking clear (or visiting /profile) should reset filters."""
    # First filter
    auth_client.get('/profile?start_date=2026-04-01&end_date=2026-04-15')
    
    # Now visit /profile without params
    response = auth_client.get('/profile')
    assert b'3' in response.data # Back to all transactions
    assert b'600.00' in response.data

def test_profile_quick_filters(auth_client):
    """
    Verify that quick filter buttons (This Month, Last Month, etc.) 
    apply correct date ranges and active styling.
    """
    today = datetime.now()
    
    # 1. Test "This Month"
    this_month_start = today.replace(day=1).strftime('%Y-%m-%d')
    response = auth_client.get('/profile?range=this_month')
    assert response.status_code == 200
    assert b'active">This Month</a>' in response.data
    assert f'value="{this_month_start}"'.encode() in response.data
    
    # 2. Test "Last Month"
    last_month_end = today.replace(day=1) - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1).strftime('%Y-%m-%d')
    response = auth_client.get('/profile?range=last_month')
    assert b'active">Last Month</a>' in response.data
    assert f'value="{last_month_start}"'.encode() in response.data
    
    # 3. Test "Last 3 Months"
    three_months_ago = (today - timedelta(days=90)).strftime('%Y-%m-%d')
    response = auth_client.get('/profile?range=last_3_months')
    assert b'active">Last 3 Months</a>' in response.data
    assert f'value="{three_months_ago}"'.encode() in response.data
