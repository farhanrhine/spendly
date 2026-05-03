# Spec: Add New Expenses

## Overview
This feature enables authenticated users to add new expense transactions to their account. Users will access a form to record expenses by entering an amount, selecting a category, providing a description, and selecting a date. The form will validate inputs and persist the expense data to the SQLite database. This is a core feature of the Finlo expense tracker, allowing users to build their transaction history.

## Depends on
- Step 1: Database setup (expenses table already exists with required columns)
- Step 3: Login and logout authentication (requires authenticated session to add expenses)

## Routes
- `GET /expenses/add` — Display the expense entry form (authenticated users only)
- `POST /expenses/add` — Process the form submission, validate inputs, save to database, and redirect to profile page (authenticated users only)

## Database changes
No database changes.
(The `expenses` table already exists with columns: `id`, `user_id`, `amount`, `category`, `date`, `description`, `created_at`)

## Templates
- **Create:** `templates/add_expense.html` — A form to capture expense details (amount, category dropdown, description, date picker) that extends `base.html`

## Files to change
- `app.py` (implement GET `/expenses/add` route to render the form, and POST `/expenses/add` route to handle form submission with validation)
- `database/queries.py` (add `create_expense()` function to insert expense record into database)

## Files to create
- `templates/add_expense.html` (expense entry form template)

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
- Form must validate:
  - Amount is required and must be a positive number
  - Category is required (provide predefined list: Food, Transport, Bills, Health, Entertainment, Other)
  - Description is optional but recommended
  - Date is required and must be a valid date (YYYY-MM-DD format)
- Date input should default to today's date
- After successful submission, redirect to `/profile` page
- Use CSS Flexbox for responsive form layout
- Form inputs should be styled consistently with existing form styles in `style.css`
- Category dropdown should render a `<select>` element with predefined options

## Definition of done
- [ ] GET `/expenses/add` renders a form with amount input, category dropdown, description textarea, and date picker
- [ ] The date input defaults to today's date
- [ ] POST `/expenses/add` validates that amount is a positive number, category is selected, and date is valid
- [ ] If validation fails, the form re-renders with error messages and preserved field values
- [ ] If validation succeeds, the expense is saved to the database with the authenticated user's ID
- [ ] After successful submission, the user is redirected to the profile page
- [ ] Only authenticated users can access GET or POST `/expenses/add` (unauthenticated users are redirected to login)
- [ ] The form is accessible and styled consistently with the rest of the application (Flexbox layout, CSS variables)
- [ ] All internal links and form actions use `url_for()` (no hardcoded URLs)
