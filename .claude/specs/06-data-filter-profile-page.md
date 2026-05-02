# Spec: Data Filter For Profile Page

## Overview
This feature adds date filtering capabilities to the user profile page. Currently, the profile page displays all-time statistics, transactions, and category breakdowns. This update will allow users to filter their financial data by specific date ranges (e.g., a start date and an end date) to gain better insights into their spending habits over specific periods.

## Depends on
- Step 05: Connect profile page to database

## Routes
No new routes.
(The existing `GET /profile` route will be modified to accept query parameters for date filtering, e.g., `?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`).

## Database changes
No database changes.

## Templates
- **Modify:** `templates/profile.html` — Add a date filter UI (start date and end date inputs inside a GET form) and ensure the selected dates persist in the form fields after submission.

## Files to change
- `app.py` (modify `/profile` route to handle `start_date` and `end_date` query parameters and pass them to database functions)
- `database/queries.py` (modify `get_summary_stats`, `get_recent_transactions`, and `get_category_breakdown` to accept optional `start_date` and `end_date` parameters)
- `templates/profile.html` (add the filter UI)

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use a standard HTML GET form for the date filter (no JavaScript required for submission).
- Ensure date formats are handled correctly (YYYY-MM-DD) in SQLite queries.

## Definition of done
- [ ] The profile page includes a form to select a start date and end date.
- [ ] Submitting the filter form updates the URL with `start_date` and `end_date` parameters and reloads the profile page.
- [ ] Total spent, recent transactions, and category breakdown accurately reflect only the data within the selected date range.
- [ ] The selected dates remain visible in the input fields after the page reloads.
- [ ] If no dates are provided, the page defaults to showing all-time data.
