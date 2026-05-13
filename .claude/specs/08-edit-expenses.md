# Spec: Edit Expenses

## Overview
This feature enables authenticated users to edit existing expense transactions. Users will access an edit form pre-populated with the current expense details (amount, category, description, date), make changes, and submit to update the database. The form will validate inputs identically to the add expense feature and persist changes back to the SQLite database. This completes the core CRUD operations for the Finlo expense tracker, allowing users to maintain accurate transaction records.

## Depends on
- Step 1: Database setup (expenses table with all required columns)
- Step 3: Login and logout authentication (requires authenticated session to edit expenses)
- Step 7: Add new expenses (reuses expense form template and validation patterns)

## Routes
- `GET /expenses/<id>/edit` — Display the expense edit form pre-populated with current data (authenticated users only)
- `POST /expenses/<id>/edit` — Process the form submission, validate inputs, update database, and redirect to profile page (authenticated users only)

## Database changes
No database changes.
(The `expenses` table already exists with all required columns: `id`, `user_id`, `amount`, `category`, `date`, `description`, `created_at`)

## Templates
- **Modify:** `templates/add_expense.html` — Reuse existing form template (can accept optional pre-filled values and submit to different endpoint based on context)
- **Alternative:** Create `templates/edit_expense.html` — A form to modify expense details (amount, category dropdown, description, date picker) that extends `base.html` and reuses most markup from add_expense.html

Choose one approach:
1. **Simpler**: Modify `add_expense.html` to handle both add and edit modes (recommended for DRY)
2. **Cleaner Separation**: Create dedicated `edit_expense.html` template

## Files to change
- `app.py` (implement GET `/expenses/<id>/edit` route to render the form with pre-populated data, and POST `/expenses/<id>/edit` route to handle form submission with validation and update)
- `database/queries.py` (add `get_expense_by_id()` function to fetch a single expense by ID, and `update_expense()` function to update expense record in database)

## Files to create
- `templates/edit_expense.html` (expense edit form template) — OR modify existing `add_expense.html` if using shared template approach

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only with `?` placeholders
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- All internal links use `url_for()` — never hardcode URLs
- Routes must check `session.get('user_id')` and redirect to login if not authenticated
- **Ownership validation**: Before rendering or updating an expense, verify that the expense `user_id` matches the authenticated user's `user_id`. Return 404 if user does not own the expense.
- Form must validate identically to add expense:
  - Amount is required and must be a positive number
  - Category is required (predefined list: Food, Transport, Bills, Health, Entertainment, Other)
  - Description is optional
  - Date is required and must be a valid date (YYYY-MM-DD format)
  - Date must not be before 2000-01-01 or in the future
- After successful update, redirect to `/profile` page
- Use CSS Flexbox for responsive form layout
- Form inputs should be styled consistently with existing form styles in `style.css`
- Category dropdown should render a `<select>` element with predefined options
- Implement CSRF protection identically to add_expense (use `session.get('csrf_token')`)
- Display the expense's original `date` value in the date input field (pre-filled)

## Definition of done
- [ ] GET `/expenses/<id>/edit` renders a form with pre-populated values from the database (amount, category, description, date)
- [ ] The date input displays the current expense's date (pre-filled in YYYY-MM-DD format)
- [ ] If the expense ID does not exist or is not owned by the authenticated user, return a 404 error
- [ ] POST `/expenses/<id>/edit` validates that amount is a positive number, category is selected, and date is valid
- [ ] POST `/expenses/<id>/edit` validates that the expense belongs to the authenticated user (ownership check)
- [ ] If validation fails, the form re-renders with error messages and preserved field values
- [ ] If validation succeeds, the expense record is updated in the database with the new values
- [ ] After successful update, the user is redirected to the profile page
- [ ] Only authenticated users can access GET or POST `/expenses/<id>/edit` (unauthenticated users are redirected to login)
- [ ] The form is accessible and styled consistently with the rest of the application (Flexbox layout, CSS variables)
- [ ] All internal links and form actions use `url_for()` (no hardcoded URLs)
- [ ] CSRF token validation is performed identically to add_expense feature
- [ ] Ownership validation prevents one user from editing another user's expenses
