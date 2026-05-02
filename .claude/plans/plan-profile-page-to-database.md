# Implementation Plan: Connect Profile Page to Database (Step 5)

## Context

This plan implements Step 5 of the Finlo project, which requires replacing the current hardcoded data in the `/profile` route with dynamic data fetched from the SQLite database. The goal is to display user-specific information (user details, expenses, categories) instead of static demo data.

## Recommended Approach

1. **Database Query Helpers (database/queries.py)**
   - Create 4 new query functions:
     - `get_user_by_id(user_id)` - Fetches user details
     - `get_summary_stats(user_id)` - Calculates total spent, transaction count, top category
     - `get_recent_transactions(user_id)` - Retrieves last 10 transactions
     - `get_category_breakdown(user_id)` - Calculates category percentages
   - All queries must use `get_db()` with parameterized SQL

2. **Route Modification (app.py)**
   - Update the `/profile` route to:
     - Fetch user data using `get_user_by_id()`
     - Pass all dynamic data to the template via Jinja2
   - Maintain existing authentication guard

3. **Template Updates (templates/profile.html)**
   - Remove hardcoded values in all 4 sections
   - Update to use dynamic Jinja variables
   - Ensure ₹ symbol is used for all amounts

## Critical Files
- `app.py` (Route handler)
- `templates/profile.html` (Template logic)
- `database/queries.py` (New file to create)

## Verification Steps
1. Log in as demo@Finlo.com/demo123
2. Verify profile shows:
   - User name/email matching database record
   - Total spent equals sum of all expenses (₹3,450.00)
   - 8 transactions in newest-first order
   - Category breakdown percentages sum to 100%
3. Test new user: Register and check profile shows zero values correctly
4. Confirm ₹ symbol displays consistently in all amounts

## Validation Rules
- All SQL queries must use `?` placeholders
- Connection must close after each query execution
- Template must handle empty data gracefully
- Percentage calculation must use integer rounding

## Testing Scope
- Unit tests for query helpers
- Route tests for authenticated access
- Seed data validation (verify 8 expenses match demo data)

## Risk Mitigation
- No database changes required during this step
- Template modifications must maintain CSS variable compliance
- Decimal-to-₹ conversion must use fixed symbol positioning