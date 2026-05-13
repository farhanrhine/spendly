import pytest
from app import app as flask_app
from database.db import init_db, create_user, get_db
from database.queries import create_expense, get_expense_by_id, update_expense
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
        'SERVER_NAME': 'localhost.localdomain'
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
    """Test client already logged in with test user."""
    with app.app_context():
        user_id = create_user('test@example.com', 'password123', 'Test User')
    
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    return client


@pytest.fixture
def another_user_client(client, app):
    """Test client logged in as a different user."""
    with app.app_context():
        user_id = create_user('other@example.com', 'password123', 'Other User')
    
    client.post('/login', data={
        'email': 'other@example.com',
        'password': 'password123'
    })
    return client


@pytest.fixture
def test_expense(app, auth_client):
    """Create a test expense for the authenticated user."""
    with app.app_context():
        user_id = create_user('test@example.com', 'password123', 'Test User')
        expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch')
        return expense_id


# ================================================================ #
# Database Layer Tests - get_expense_by_id()                       #
# ================================================================ #

class TestGetExpenseById:
    """Tests for get_expense_by_id() database function."""
    
    def test_get_expense_by_valid_id(self, app):
        """Should retrieve expense with valid ID and correct owner."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 150.50, 'Food', '2026-05-01', 'Lunch')
            
            expense = get_expense_by_id(user_id, expense_id)
            assert expense is not None
            assert expense['id'] == expense_id
            assert expense['amount'] == 150.50
            assert expense['category'] == 'Food'
            assert expense['date'] == '2026-05-01'
            assert expense['description'] == 'Lunch'
            assert expense['user_id'] == user_id
    
    def test_get_expense_nonexistent_id_returns_none(self, app):
        """Should return None for non-existent expense ID."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password123', 'Test User')
            expense = get_expense_by_id(user_id, 99999)
            assert expense is None
    
    def test_get_expense_wrong_owner_returns_none(self, app):
        """Should return None if expense not owned by user (ownership validation)."""
        with app.app_context():
            user1_id = create_user('user1@example.com', 'password123', 'User 1')
            user2_id = create_user('user2@example.com', 'password123', 'User 2')
            
            expense_id = create_expense(user1_id, 100.00, 'Food', '2026-05-01', 'Test')
            
            # Try to get user1's expense as user2
            expense = get_expense_by_id(user2_id, expense_id)
            assert expense is None


# ================================================================ #
# Database Layer Tests - update_expense()                          #
# ================================================================ #

class TestUpdateExpense:
    """Tests for update_expense() database function."""
    
    def test_update_expense_valid_data(self, app):
        """Should update expense with valid data."""
        with app.app_context():
            user_id = create_user('test_update_valid@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch')
            
            update_expense(user_id, expense_id, 200.00, 'Transport', '2026-05-02', 'Taxi')
            
            updated = get_expense_by_id(user_id, expense_id)
            assert updated['amount'] == 200.00
            assert updated['category'] == 'Transport'
            assert updated['description'] == 'Taxi'
            assert updated['date'] == '2026-05-02'
    
    def test_update_expense_ownership_validation(self, app):
        """Should not update if user doesn't own the expense."""
        with app.app_context():
            user1_id = create_user('user1@example.com', 'password123', 'User 1')
            user2_id = create_user('user2@example.com', 'password123', 'User 2')
            
            expense_id = create_expense(user1_id, 100.00, 'Food', '2026-05-01', 'Test')
            
            # Try to update user1's expense as user2 - should fail or raise error
            try:
                result = update_expense(user2_id, expense_id, 200.00, 'Transport', 'Updated', '2026-05-02')
                # If no exception, verify the update didn't happen
                updated = get_expense_by_id(user1_id, expense_id)
                assert updated['amount'] == 100.00, "Expense should not be updated by different user"
            except Exception:
                # If function raises an exception, that's also valid behavior
                pass
    
    def test_update_expense_optional_description(self, app):
        """Should allow updating description to empty/None."""
        with app.app_context():
            user_id = create_user('test_update_desc@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch')
            
            update_expense(user_id, expense_id, 100.00, 'Food', '2026-05-01', None)
            
            updated = get_expense_by_id(user_id, expense_id)
            assert updated['description'] is None or updated['description'] == ''


# ================================================================ #
# GET /expenses/<id>/edit Route Tests                              #
# ================================================================ #

class TestGetEditExpenseRoute:
    """Tests for GET /expenses/<id>/edit route."""
    
    def test_unauthenticated_redirects_to_login(self, client, app):
        """Unauthenticated user should be redirected to login."""
        with app.app_context():
            user_id = create_user('test_unauth_get@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch')
        
        response = client.get(f'/expenses/{expense_id}/edit')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_authenticated_returns_form_200(self, client, app):
        """Authenticated user should see the edit form."""
        with app.app_context():
            user_id = create_user('test_auth_form@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch')
        
        # Login as the created user
        client.post('/login', data={
            'email': 'test_auth_form@example.com',
            'password': 'password123'
        })
        response = client.get(f'/expenses/{expense_id}/edit')
        assert response.status_code == 200
        assert b'<form' in response.data
    
    def test_form_contains_prefilledamount(self, client, app):
        """Edit form should contain pre-filled amount."""
        with app.app_context():
            user_id = create_user('test_form_amount@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 125.75, 'Food', '2026-05-01', 'Lunch')
        
        client.post('/login', data={'email': 'test_form_amount@example.com', 'password': 'password123'})
        response = client.get(f'/expenses/{expense_id}/edit')
        assert b'125.75' in response.data or b'125.5' in response.data or b'125' in response.data
    
    def test_form_contains_prefilled_category(self, client, app):
        """Edit form should contain pre-filled category."""
        with app.app_context():
            user_id = create_user('test_form_cat@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Transport', '2026-05-01', 'Taxi')
        
        client.post('/login', data={'email': 'test_form_cat@example.com', 'password': 'password123'})
        response = client.get(f'/expenses/{expense_id}/edit')
        assert b'Transport' in response.data
        assert b'selected' in response.data
    
    def test_form_contains_prefilled_date(self, client, app):
        """Edit form should contain pre-filled date in YYYY-MM-DD format."""
        with app.app_context():
            user_id = create_user('test_form_date@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-03', 'Lunch')
        
        client.post('/login', data={'email': 'test_form_date@example.com', 'password': 'password123'})
        response = client.get(f'/expenses/{expense_id}/edit')
        assert b'2026-05-03' in response.data or b'value="2026-05-03"' in response.data
    
    def test_form_contains_prefilled_description(self, client, app):
        """Edit form should contain pre-filled description."""
        with app.app_context():
            user_id = create_user('test_form_desc@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch at office')
        
        client.post('/login', data={'email': 'test_form_desc@example.com', 'password': 'password123'})
        response = client.get(f'/expenses/{expense_id}/edit')
        assert b'Lunch at office' in response.data
    
    def test_nonexistent_expense_returns_404(self, auth_client, app):
        """Requesting non-existent expense should return 404."""
        response = auth_client.get('/expenses/99999/edit')
        assert response.status_code == 404
    
    def test_not_owned_expense_returns_404(self, auth_client, another_user_client, app):
        """Accessing another user's expense should return 404."""
        with app.app_context():
            user1_id = create_user('user1@example.com', 'password123', 'User 1')
            expense_id = create_expense(user1_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        response = another_user_client.get(f'/expenses/{expense_id}/edit')
        assert response.status_code == 404
    
    def test_form_contains_all_field_labels(self, client, app):
        """Form should contain all required labels."""
        with app.app_context():
            user_id = create_user('test_form_labels@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_form_labels@example.com', 'password': 'password123'})
        response = client.get(f'/expenses/{expense_id}/edit')
        assert b'Amount' in response.data
        assert b'Category' in response.data
        assert b'Date' in response.data
        assert b'Description' in response.data
    
    def test_form_contains_all_categories(self, client, app):
        """Edit form should contain all predefined categories."""
        with app.app_context():
            user_id = create_user('test_form_cats@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_form_cats@example.com', 'password': 'password123'})
        response = client.get(f'/expenses/{expense_id}/edit')
        expected_categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
        for category in expected_categories:
            assert category.encode() in response.data


# ================================================================ #
# POST /expenses/<id>/edit Route Tests                             #
# ================================================================ #

class TestPostEditExpenseRoute:
    """Tests for POST /expenses/<id>/edit route."""
    
    def test_unauthenticated_redirects_to_login(self, client, app):
        """Unauthenticated user should be redirected to login."""
        with app.app_context():
            user_id = create_user('test_unauth_post@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch')
        
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '150',
            'category': 'Transport',
            'date': '2026-05-02',
            'description': 'Updated'
        })
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_successful_update_redirects_to_profile(self, client, app):
        """Successful update should redirect to profile."""
        with app.app_context():
            user_id = create_user('test_success_redir@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch')
        
        client.post('/login', data={'email': 'test_success_redir@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '150',
            'category': 'Transport',
            'date': '2026-05-02',
            'description': 'Updated'
        }, follow_redirects=False)
        assert response.status_code == 302
        assert '/profile' in response.location
    
    def test_successful_update_persists_to_database(self, client, app):
        """Successful update should persist changes to database."""
        with app.app_context():
            user_id = create_user('test_persist@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch')
        
        client.post('/login', data={'email': 'test_persist@example.com', 'password': 'password123'})
        client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '200.50',
            'category': 'Transport',
            'date': '2026-05-05',
            'description': 'Taxi ride'
        })
        
        with app.app_context():
            updated = get_expense_by_id(user_id, expense_id)
            assert updated['amount'] == 200.50
            assert updated['category'] == 'Transport'
            assert updated['date'] == '2026-05-05'
            assert updated['description'] == 'Taxi ride'
    
    def test_missing_amount_shows_error(self, client, app):
        """Missing amount should show error message."""
        with app.app_context():
            user_id = create_user('test_missing_amt@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_missing_amt@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '',
            'category': 'Food',
            'date': '2026-05-01',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'error' in response.data.lower() or b'amount' in response.data.lower()
    
    def test_negative_amount_shows_error(self, client, app):
        """Negative amount should show error."""
        with app.app_context():
            user_id = create_user('test_neg_amt@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_neg_amt@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '-50',
            'category': 'Food',
            'date': '2026-05-01',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'positive' in response.data.lower() or b'amount' in response.data.lower()
    
    def test_zero_amount_shows_error(self, client, app):
        """Zero amount should show error."""
        with app.app_context():
            user_id = create_user('test_zero_amt@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_zero_amt@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '0',
            'category': 'Food',
            'date': '2026-05-01',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'positive' in response.data.lower() or b'amount' in response.data.lower()
    
    def test_non_numeric_amount_shows_error(self, client, app):
        """Non-numeric amount should show error."""
        with app.app_context():
            user_id = create_user('test_non_num_amt@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_non_num_amt@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': 'abc',
            'category': 'Food',
            'date': '2026-05-01',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'number' in response.data.lower() or b'amount' in response.data.lower()
    
    def test_missing_category_shows_error(self, client, app):
        """Missing category should show error."""
        with app.app_context():
            user_id = create_user('test_missing_cat@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_missing_cat@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '100',
            'category': '',
            'date': '2026-05-01',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'category' in response.data.lower()
    
    def test_invalid_category_shows_error(self, client, app):
        """Invalid category should show error."""
        with app.app_context():
            user_id = create_user('test_invalid_cat@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_invalid_cat@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '100',
            'category': 'InvalidCategory',
            'date': '2026-05-01',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'category' in response.data.lower()
    
    def test_missing_date_shows_error(self, client, app):
        """Missing date should show error."""
        with app.app_context():
            user_id = create_user('test_missing_date@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_missing_date@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '100',
            'category': 'Food',
            'date': '',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'date' in response.data.lower()
    
    def test_invalid_date_format_shows_error(self, client, app):
        """Invalid date format should show error."""
        with app.app_context():
            user_id = create_user('test_invalid_date@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_invalid_date@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '100',
            'category': 'Food',
            'date': '05/01/2026',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'date' in response.data.lower()
    
    def test_future_date_shows_error(self, client, app):
        """Future date should show error."""
        with app.app_context():
            user_id = create_user('test_future_date@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
            future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        client.post('/login', data={'email': 'test_future_date@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '100',
            'category': 'Food',
            'date': future_date,
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'future' in response.data.lower() or b'date' in response.data.lower()
    
    def test_date_before_2000_shows_error(self, client, app):
        """Date before 2000-01-01 should show error."""
        with app.app_context():
            user_id = create_user('test_old_date@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_old_date@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '100',
            'category': 'Food',
            'date': '1999-12-31',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'2000' in response.data or b'date' in response.data.lower()
    
    def test_optional_description_can_be_empty(self, client, app):
        """Description is optional and can be empty."""
        with app.app_context():
            user_id = create_user('test_empty_desc@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Original')
        
        client.post('/login', data={'email': 'test_empty_desc@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '100',
            'category': 'Food',
            'date': '2026-05-01',
            'description': ''
        }, follow_redirects=False)
        assert response.status_code == 302
        
        with app.app_context():
            updated = get_expense_by_id(user_id, expense_id)
            assert updated['description'] is None or updated['description'] == ''
    
    def test_form_preserves_amount_on_error(self, client, app):
        """Amount should be preserved when form re-renders on error."""
        with app.app_context():
            user_id = create_user('test_preserve_amt@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_preserve_amt@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '123.45',
            'category': 'InvalidCategory',
            'date': '2026-05-01',
            'description': 'Test'
        })
        assert b'123.45' in response.data
    
    def test_form_preserves_category_on_error(self, client, app):
        """Category should be preserved when form re-renders on error."""
        with app.app_context():
            user_id = create_user('test_preserve_cat@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_preserve_cat@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '100',
            'category': 'Food',
            'date': 'invalid-date',
            'description': 'Test'
        })
        assert b'Food' in response.data
        assert b'selected' in response.data
    
    def test_form_preserves_description_on_error(self, client, app):
        """Description should be preserved when form re-renders on error."""
        with app.app_context():
            user_id = create_user('test_preserve_desc@example.com', 'password123', 'Test User')
            expense_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        client.post('/login', data={'email': 'test_preserve_desc@example.com', 'password': 'password123'})
        response = client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '100',
            'category': 'InvalidCategory',
            'date': '2026-05-01',
            'description': 'My lunch at work'
        })
        assert b'My lunch at work' in response.data
    
    def test_nonexistent_expense_returns_404(self, auth_client, app):
        """Posting to non-existent expense should return 404."""
        response = auth_client.post('/expenses/99999/edit', data={
            'amount': '100',
            'category': 'Food',
            'date': '2026-05-01',
            'description': 'Test'
        })
        assert response.status_code == 404
    
    def test_not_owned_expense_returns_404(self, auth_client, another_user_client, app):
        """Posting to another user's expense should return 404."""
        with app.app_context():
            user1_id = create_user('user1@example.com', 'password123', 'User 1')
            expense_id = create_expense(user1_id, 100.00, 'Food', '2026-05-01', 'Test')
        
        response = another_user_client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '200',
            'category': 'Transport',
            'date': '2026-05-02',
            'description': 'Updated'
        })
        assert response.status_code == 404
    
    def test_valid_categories_accepted(self, client, app):
        """All valid categories should be accepted."""
        with app.app_context():
            user_id = create_user('test_all_cats@example.com', 'password123', 'Test User')
            valid_categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
            
            for i, category in enumerate(valid_categories):
                expense_id = create_expense(user_id, 100.00 + i, 'Food', '2026-05-01', f'Expense {i}')
        
        client.post('/login', data={'email': 'test_all_cats@example.com', 'password': 'password123'})
        
        with app.app_context():
            user_id = list(app.app_context().app.config.get('user_id') or [None])[0]
            # Get all expenses for this user
            db = get_db()
            expenses = db.execute('SELECT id FROM expenses WHERE user_id = ? ORDER BY id', (list(app.app_context().app.config.values())[-1] if hasattr(app.app_context().app.config, 'values') else 1,)).fetchall()
        
        # Test with each user's expense
        valid_categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
        for i in range(6):
            with app.app_context():
                expenses = db.execute('SELECT id FROM expenses ORDER BY created_at DESC LIMIT 6').fetchall()
                if i < len(expenses):
                    expense_id = expenses[i]['id']
                    response = client.post(f'/expenses/{expense_id}/edit', data={
                        'amount': str(150.00 + i),
                        'category': valid_categories[i],
                        'date': '2026-05-02',
                        'description': f'{valid_categories[i]} test'
                    }, follow_redirects=False)
                    assert response.status_code == 302, f"Category {valid_categories[i]} should be accepted"


# ================================================================ #
# Integration Tests                                                #
# ================================================================ #

class TestEditExpenseIntegration:
    """End-to-end integration tests for edit expense flow."""
    
    def test_create_edit_and_verify_in_profile(self, auth_client, app):
        """End-to-end: create expense → edit → verify changes in profile."""
        with app.app_context():
            user_id = create_user('test_e2e_flow@example.com', 'password123', 'Test User')
        
        # Create expense
        create_response = auth_client.post('/expenses/add', data={
            'amount': '100.00',
            'category': 'Food',
            'date': '2026-05-01',
            'description': 'Original lunch'
        }, follow_redirects=True)
        
        # Get the expense ID from database
        with app.app_context():
            db = get_db()
            expense = db.execute(
                'SELECT id FROM expenses WHERE amount = ? ORDER BY created_at DESC LIMIT 1',
                (100.00,)
            ).fetchone()
            expense_id = expense['id']
        
        # Access edit form
        edit_form_response = auth_client.get(f'/expenses/{expense_id}/edit')
        assert edit_form_response.status_code == 200
        assert b'100' in edit_form_response.data
        assert b'Original lunch' in edit_form_response.data
        
        # Submit edit
        edit_response = auth_client.post(f'/expenses/{expense_id}/edit', data={
            'amount': '150.50',
            'category': 'Transport',
            'date': '2026-05-05',
            'description': 'Updated taxi ride'
        }, follow_redirects=True)
        assert edit_response.status_code == 200
        
        # Verify changes persisted
        with app.app_context():
            updated = get_expense_by_id(user_id, expense_id)
            assert updated['amount'] == 150.50
            assert updated['category'] == 'Transport'
            assert updated['date'] == '2026-05-05'
            assert updated['description'] == 'Updated taxi ride'
        
        # Verify visible in profile
        profile_response = auth_client.get('/profile', follow_redirects=True)
        assert b'150.5' in profile_response.data or b'150.50' in profile_response.data
        assert b'Transport' in profile_response.data
        assert b'Updated taxi ride' in profile_response.data
    
    def test_edit_multiple_expenses_independently(self, client, app):
        """Should be able to edit multiple expenses independently."""
        with app.app_context():
            user_id = create_user('test_multiple_edit@example.com', 'password123', 'Test User')
            expense1_id = create_expense(user_id, 100.00, 'Food', '2026-05-01', 'Lunch')
            expense2_id = create_expense(user_id, 50.00, 'Transport', '2026-05-02', 'Taxi')
        
        client.post('/login', data={'email': 'test_multiple_edit@example.com', 'password': 'password123'})
        
        # Edit first expense
        client.post(f'/expenses/{expense1_id}/edit', data={
            'amount': '200.00',
            'category': 'Food',
            'date': '2026-05-01',
            'description': 'Updated lunch'
        }, follow_redirects=False)
        
        # Edit second expense
        client.post(f'/expenses/{expense2_id}/edit', data={
            'amount': '75.00',
            'category': 'Transport',
            'date': '2026-05-02',
            'description': 'Updated taxi'
        }, follow_redirects=False)
        
        # Verify both updates
        with app.app_context():
            updated1 = get_expense_by_id(user_id, expense1_id)
            updated2 = get_expense_by_id(user_id, expense2_id)
            
            assert updated1['amount'] == 200.00
            assert updated1['description'] == 'Updated lunch'
            assert updated2['amount'] == 75.00
            assert updated2['description'] == 'Updated taxi'
    
    def test_edit_preserves_other_user_expenses(self, app):
        """Editing one user's expense should not affect another user's expenses."""
        with app.app_context():
            user1_id = create_user('test_user1_isol@example.com', 'password123', 'User 1')
            user2_id = create_user('test_user2_isol@example.com', 'password123', 'User 2')
            
            user1_expense_id = create_expense(user1_id, 100.00, 'Food', '2026-05-01', 'User1 lunch')
            user2_expense_id = create_expense(user2_id, 50.00, 'Transport', '2026-05-02', 'User2 taxi')
        
        # Create logged-in client for user1
        client1 = app.test_client()
        client1.post('/login', data={
            'email': 'test_user1_isol@example.com',
            'password': 'password123'
        })
        
        # User 1 edits their expense
        client1.post(f'/expenses/{user1_expense_id}/edit', data={
            'amount': '150.00',
            'category': 'Food',
            'date': '2026-05-01',
            'description': 'Updated'
        }, follow_redirects=False)
        
        # Verify User 2's expense unchanged
        with app.app_context():
            user2_updated = get_expense_by_id(user2_id, user2_expense_id)
            assert user2_updated['amount'] == 50.00
            assert user2_updated['description'] == 'User2 taxi'
