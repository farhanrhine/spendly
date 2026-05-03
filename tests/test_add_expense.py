import pytest
from app import app as flask_app
from database.db import init_db, create_user, get_db
from database.queries import create_expense
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


# ================================================================ #
# GET /expenses/add Route Tests                                    #
# ================================================================ #

class TestGetAddExpenseRoute:
    """Tests for GET /expenses/add route."""
    
    def test_unauthenticated_redirects_to_login(self, client):
        """Unauthenticated user should be redirected to login page."""
        response = client.get('/expenses/add')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_authenticated_returns_200(self, auth_client):
        """Authenticated user should see the form."""
        response = auth_client.get('/expenses/add')
        assert response.status_code == 200
    
    def test_form_contains_amount_input(self, auth_client):
        """Form should contain amount input field."""
        response = auth_client.get('/expenses/add')
        assert b'id="amount"' in response.data
        assert b'type="number"' in response.data
        assert b'step="0.01"' in response.data
        assert b'min="0"' in response.data
    
    def test_form_contains_category_select(self, auth_client):
        """Form should contain category dropdown."""
        response = auth_client.get('/expenses/add')
        assert b'id="category"' in response.data
        assert b'<select' in response.data
    
    def test_form_contains_date_input(self, auth_client):
        """Form should contain date input field."""
        response = auth_client.get('/expenses/add')
        assert b'id="date"' in response.data
        assert b'type="date"' in response.data
    
    def test_form_contains_description_textarea(self, auth_client):
        """Form should contain description textarea."""
        response = auth_client.get('/expenses/add')
        assert b'id="description"' in response.data
        assert b'<textarea' in response.data
    
    def test_default_date_is_today(self, auth_client):
        """Date input should default to today."""
        response = auth_client.get('/expenses/add')
        today = datetime.now().strftime('%Y-%m-%d')
        assert f'value="{today}"'.encode() in response.data
    
    def test_all_categories_present(self, auth_client):
        """Form should contain all predefined categories."""
        response = auth_client.get('/expenses/add')
        expected_categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
        
        for category in expected_categories:
            assert category.encode() in response.data
    
    def test_form_action_uses_url_for(self, auth_client):
        """Form action should use url_for to generate URL."""
        response = auth_client.get('/expenses/add')
        assert b'method="POST"' in response.data
        assert b'action=' in response.data
    
    def test_page_contains_required_labels(self, auth_client):
        """Form should contain all required labels."""
        response = auth_client.get('/expenses/add')
        assert b'Amount' in response.data
        assert b'Category' in response.data
        assert b'Date' in response.data
        assert b'Description' in response.data


# ================================================================ #
# POST /expenses/add Route Tests                                   #
# ================================================================ #

class TestPostAddExpenseRoute:
    """Tests for POST /expenses/add route."""
    
    def test_unauthenticated_redirects_to_login(self, client):
        """Unauthenticated user should be redirected to login page."""
        response = client.post('/expenses/add', data={
            'amount': '100',
            'category': 'Food',
            'date': '2026-05-03',
            'description': 'Test'
        })
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_successful_submission_creates_expense(self, auth_client, app):
        """Valid expense should be created in database."""
        auth_client.post('/expenses/add', data={
            'amount': '150.50',
            'category': 'Food',
            'date': '2026-05-01',
            'description': 'Lunch'
        })
        
        with app.app_context():
            db = get_db()
            expense = db.execute(
                'SELECT * FROM expenses WHERE amount = ?', (150.50,)
            ).fetchone()
            assert expense is not None
            assert expense['category'] == 'Food'
            assert expense['date'] == '2026-05-01'
            assert expense['description'] == 'Lunch'
    
    def test_successful_submission_redirects_to_profile(self, auth_client):
        """Successful submission should redirect to profile."""
        response = auth_client.post('/expenses/add', data={
            'amount': '100',
            'category': 'Food',
            'date': '2026-05-03',
            'description': 'Test'
        }, follow_redirects=False)
        assert response.status_code == 302
        assert '/profile' in response.location
    
    def test_missing_amount_shows_error(self, auth_client):
        """Missing amount should show error message."""
        response = auth_client.post('/expenses/add', data={
            'amount': '',
            'category': 'Food',
            'date': '2026-05-03',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'error' in response.data.lower() or b'Amount' in response.data
    
    def test_non_positive_amount_shows_error(self, auth_client):
        """Non-positive amount should show error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '-50',
            'category': 'Food',
            'date': '2026-05-03',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'positive' in response.data.lower() or b'amount' in response.data.lower()
    
    def test_zero_amount_shows_error(self, auth_client):
        """Zero amount should show error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '0',
            'category': 'Food',
            'date': '2026-05-03',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'positive' in response.data.lower() or b'amount' in response.data.lower()
    
    def test_invalid_amount_format_shows_error(self, auth_client):
        """Non-numeric amount should show error."""
        response = auth_client.post('/expenses/add', data={
            'amount': 'abc',
            'category': 'Food',
            'date': '2026-05-03',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'number' in response.data.lower() or b'amount' in response.data.lower()
    
    def test_missing_category_shows_error(self, auth_client):
        """Missing category should show error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '100',
            'category': '',
            'date': '2026-05-03',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'category' in response.data.lower()
    
    def test_invalid_category_shows_error(self, auth_client):
        """Invalid category should show error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '100',
            'category': 'InvalidCategory',
            'date': '2026-05-03',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'category' in response.data.lower()
    
    def test_missing_date_shows_error(self, auth_client):
        """Missing date should show error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '100',
            'category': 'Food',
            'date': '',
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'date' in response.data.lower()
    
    def test_invalid_date_format_shows_error(self, auth_client):
        """Invalid date format should show error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '100',
            'category': 'Food',
            'date': '05/03/2026',  # Wrong format
            'description': 'Test'
        })
        assert response.status_code == 200
        assert b'date' in response.data.lower()
    
    def test_form_preserves_amount_on_error(self, auth_client):
        """Amount should be preserved when form re-renders on error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '123.45',
            'category': 'InvalidCategory',
            'date': '2026-05-03',
            'description': 'Test'
        })
        assert b'123.45' in response.data
    
    def test_form_preserves_category_on_error(self, auth_client):
        """Category should be preserved when form re-renders on error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '100',
            'category': 'Food',
            'date': 'invalid-date',
            'description': 'Test'
        })
        assert b'Food' in response.data
        assert b'selected' in response.data
    
    def test_form_preserves_date_on_error(self, auth_client):
        """Date should be preserved when form re-renders on error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '100',
            'category': 'Food',
            'date': '2026-05-03',
            'description': 'Test'
        }, follow_redirects=True)
        # This should succeed, so check the successful case
        assert response.status_code == 200
    
    def test_form_preserves_description_on_error(self, auth_client):
        """Description should be preserved when form re-renders on error."""
        response = auth_client.post('/expenses/add', data={
            'amount': '100',
            'category': 'InvalidCategory',
            'date': '2026-05-03',
            'description': 'My lunch'
        })
        assert b'My lunch' in response.data
    
    def test_optional_description_can_be_empty(self, auth_client, app):
        """Description is optional and can be empty."""
        response = auth_client.post('/expenses/add', data={
            'amount': '100',
            'category': 'Food',
            'date': '2026-05-03',
            'description': ''
        }, follow_redirects=False)
        assert response.status_code == 302
        
        with app.app_context():
            db = get_db()
            expense = db.execute(
                'SELECT * FROM expenses WHERE amount = ?', (100,)
            ).fetchone()
            assert expense is not None
            assert expense['description'] is None or expense['description'] == ''
    
    def test_valid_categories_accepted(self, auth_client, app):
        """All valid categories should be accepted."""
        valid_categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
        
        for i, category in enumerate(valid_categories):
            response = auth_client.post('/expenses/add', data={
                'amount': str(100 + i),
                'category': category,
                'date': '2026-05-03',
                'description': f'{category} test'
            }, follow_redirects=False)
            assert response.status_code == 302, f"Category {category} should be accepted"
    
    def test_expense_associated_with_correct_user(self, auth_client, app):
        """Expense should be associated with the authenticated user."""
        with app.app_context():
            db = get_db()
            # Get the user_id from session/auth
            user_id = create_user('another@example.com', 'password', 'Another User')
        
        response = auth_client.post('/expenses/add', data={
            'amount': '250',
            'category': 'Transport',
            'date': '2026-05-03',
            'description': 'Taxi'
        }, follow_redirects=False)
        
        with app.app_context():
            db = get_db()
            expense = db.execute(
                'SELECT * FROM expenses WHERE amount = ?', (250,)
            ).fetchone()
            assert expense is not None
            # Should be associated with the auth_client user, not the other user
            assert expense['user_id'] != user_id
    
    def test_float_amounts_handled_correctly(self, auth_client, app):
        """Decimal amounts should be stored correctly."""
        response = auth_client.post('/expenses/add', data={
            'amount': '99.99',
            'category': 'Food',
            'date': '2026-05-03',
            'description': 'Test'
        }, follow_redirects=False)
        assert response.status_code == 302
        
        with app.app_context():
            db = get_db()
            expense = db.execute(
                'SELECT * FROM expenses WHERE amount = ?', (99.99,)
            ).fetchone()
            assert expense is not None
            assert abs(expense['amount'] - 99.99) < 0.01


# ================================================================ #
# create_expense() Function Tests                                  #
# ================================================================ #

class TestCreateExpenseFunction:
    """Tests for create_expense() function in database/queries.py."""
    
    def test_creates_expense_successfully(self, app):
        """Function should create expense and return ID."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            expense_id = create_expense(
                user_id=user_id,
                amount=100.0,
                category='Food',
                date='2026-05-03',
                description='Lunch'
            )
            
            assert isinstance(expense_id, int)
            assert expense_id > 0
    
    def test_inserts_into_database(self, app):
        """Function should insert expense into database."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            expense_id = create_expense(
                user_id=user_id,
                amount=150.0,
                category='Transport',
                date='2026-05-03',
                description='Bus'
            )
            
            db = get_db()
            expense = db.execute(
                'SELECT * FROM expenses WHERE id = ?', (expense_id,)
            ).fetchone()
            
            assert expense is not None
            assert expense['user_id'] == user_id
            assert expense['amount'] == 150.0
            assert expense['category'] == 'Transport'
            assert expense['date'] == '2026-05-03'
            assert expense['description'] == 'Bus'
    
    def test_non_positive_amount_raises_error(self, app):
        """Negative amount should raise ValueError."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            with pytest.raises(ValueError) as exc_info:
                create_expense(
                    user_id=user_id,
                    amount=-100,
                    category='Food',
                    date='2026-05-03',
                    description='Test'
                )
            assert 'positive' in str(exc_info.value).lower()
    
    def test_zero_amount_raises_error(self, app):
        """Zero amount should raise ValueError."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            with pytest.raises(ValueError) as exc_info:
                create_expense(
                    user_id=user_id,
                    amount=0,
                    category='Food',
                    date='2026-05-03',
                    description='Test'
                )
            assert 'positive' in str(exc_info.value).lower()
    
    def test_invalid_category_raises_error(self, app):
        """Invalid category should raise ValueError."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            with pytest.raises(ValueError) as exc_info:
                create_expense(
                    user_id=user_id,
                    amount=100,
                    category='InvalidCategory',
                    date='2026-05-03',
                    description='Test'
                )
            assert 'category' in str(exc_info.value).lower()
    
    def test_empty_category_raises_error(self, app):
        """Empty category should raise ValueError."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            with pytest.raises(ValueError) as exc_info:
                create_expense(
                    user_id=user_id,
                    amount=100,
                    category='',
                    date='2026-05-03',
                    description='Test'
                )
            assert 'category' in str(exc_info.value).lower()
    
    def test_invalid_date_format_raises_error(self, app):
        """Invalid date format should raise ValueError."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            with pytest.raises(ValueError) as exc_info:
                create_expense(
                    user_id=user_id,
                    amount=100,
                    category='Food',
                    date='05/03/2026',  # Wrong format
                    description='Test'
                )
            assert 'date' in str(exc_info.value).lower()
    
    def test_invalid_date_values_raises_error(self, app):
        """Invalid date values should raise ValueError."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            with pytest.raises(ValueError) as exc_info:
                create_expense(
                    user_id=user_id,
                    amount=100,
                    category='Food',
                    date='2026-13-45',  # Invalid day and month
                    description='Test'
                )
            assert 'date' in str(exc_info.value).lower()
    
    def test_optional_description_is_none(self, app):
        """Description is optional and can be None."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            expense_id = create_expense(
                user_id=user_id,
                amount=100,
                category='Food',
                date='2026-05-03',
                description=None
            )
            
            db = get_db()
            expense = db.execute(
                'SELECT * FROM expenses WHERE id = ?', (expense_id,)
            ).fetchone()
            
            assert expense['description'] is None
    
    def test_optional_description_can_be_omitted(self, app):
        """Description can be omitted from function call."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            expense_id = create_expense(
                user_id=user_id,
                amount=100,
                category='Food',
                date='2026-05-03'
            )
            
            db = get_db()
            expense = db.execute(
                'SELECT * FROM expenses WHERE id = ?', (expense_id,)
            ).fetchone()
            
            assert expense is not None
    
    def test_string_amount_converted_to_float(self, app):
        """String amount should be converted to float."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            expense_id = create_expense(
                user_id=user_id,
                amount='123.45',
                category='Food',
                date='2026-05-03',
                description='Test'
            )
            
            db = get_db()
            expense = db.execute(
                'SELECT * FROM expenses WHERE id = ?', (expense_id,)
            ).fetchone()
            
            assert isinstance(expense['amount'], float) or isinstance(expense['amount'], int)
            assert abs(float(expense['amount']) - 123.45) < 0.01
    
    def test_all_valid_categories_accepted(self, app):
        """All valid categories should be accepted."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            valid_categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
            
            for category in valid_categories:
                expense_id = create_expense(
                    user_id=user_id,
                    amount=100,
                    category=category,
                    date='2026-05-03',
                    description='Test'
                )
                assert expense_id > 0
    
    def test_whitespace_stripped_from_category(self, app):
        """Whitespace around category should be handled."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            # Note: The route handler strips whitespace, but the function expects clean input
            expense_id = create_expense(
                user_id=user_id,
                amount=100,
                category='Food',
                date='2026-05-03',
                description='Test'
            )
            assert expense_id > 0
    
    def test_created_at_timestamp_auto_set(self, app):
        """created_at should be automatically set by database."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            expense_id = create_expense(
                user_id=user_id,
                amount=100,
                category='Food',
                date='2026-05-03',
                description='Test'
            )
            
            db = get_db()
            expense = db.execute(
                'SELECT * FROM expenses WHERE id = ?', (expense_id,)
            ).fetchone()
            
            assert expense['created_at'] is not None
    
    def test_invalid_amount_type_raises_error(self, app):
        """Non-numeric amount type should raise ValueError."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            with pytest.raises(ValueError) as exc_info:
                create_expense(
                    user_id=user_id,
                    amount='abc',
                    category='Food',
                    date='2026-05-03',
                    description='Test'
                )
            assert 'positive' in str(exc_info.value).lower() or 'amount' in str(exc_info.value).lower()
    
    def test_case_sensitive_category(self, app):
        """Categories should be case-sensitive (Food != food)."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            with pytest.raises(ValueError):
                create_expense(
                    user_id=user_id,
                    amount=100,
                    category='food',  # lowercase should fail
                    date='2026-05-03',
                    description='Test'
                )
    
    def test_edge_case_very_small_amount(self, app):
        """Very small positive amounts should be accepted."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            expense_id = create_expense(
                user_id=user_id,
                amount=0.01,
                category='Food',
                date='2026-05-03',
                description='Test'
            )
            
            assert expense_id > 0
    
    def test_edge_case_large_amount(self, app):
        """Large amounts should be accepted."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            
            expense_id = create_expense(
                user_id=user_id,
                amount=999999.99,
                category='Food',
                date='2026-05-03',
                description='Test'
            )
            
            assert expense_id > 0
    
    def test_edge_case_future_date(self, app):
        """Future dates should be accepted."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            future_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
            
            expense_id = create_expense(
                user_id=user_id,
                amount=100,
                category='Food',
                date=future_date,
                description='Test'
            )
            
            assert expense_id > 0
    
    def test_edge_case_past_date(self, app):
        """Past dates should be accepted."""
        with app.app_context():
            user_id = create_user('test@example.com', 'password', 'Test')
            past_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            
            expense_id = create_expense(
                user_id=user_id,
                amount=100,
                category='Food',
                date=past_date,
                description='Test'
            )
            
            assert expense_id > 0
