# Implementation Plan: Data Filter For Profile Page

This plan outlines the steps required to implement the date filtering feature for the profile page, based on the `06-data-filter-profile-page.md` spec.

## Step 1: Update Database Queries (`database/queries.py`)
Modify the existing database query functions to accept optional date parameters and filter the results accordingly.

*   **`get_summary_stats(user_id, start_date=None, end_date=None)`**:
    *   Update the SQL query to include `AND date >= ?` and `AND date <= ?` conditions if `start_date` and `end_date` are provided.
    *   Ensure parameter binding matches the conditional query string.
*   **`get_recent_transactions(user_id, limit=10, start_date=None, end_date=None)`**:
    *   Update the SQL query to filter by `start_date` and `end_date` before applying the `LIMIT`.
*   **`get_category_breakdown(user_id, start_date=None, end_date=None)`**:
    *   Update the `GROUP BY` query to filter by the provided date range.

## Step 2: Update Profile Route (`app.py`)
Modify the `/profile` route to handle incoming query parameters and pass them to the database functions.

*   Extract `start_date` and `end_date` from `request.args`.
*   Validate the dates if necessary (though simple string passing to SQLite usually works for `YYYY-MM-DD`).
*   Pass `start_date` and `end_date` to `get_summary_stats`, `get_recent_transactions`, and `get_category_breakdown`.
*   Pass the extracted `start_date` and `end_date` into the template context so they can be used to pre-fill the form inputs.

## Step 3: Update Profile Template (`templates/profile.html`)
Add the user interface for the date filter.

*   Add a standard HTML `<form method="GET" action="{{ url_for('profile') }}">`.
*   Include `<input type="date" name="start_date">` and `<input type="date" name="end_date">`.
*   Set the `value` attributes of these inputs to the `start_date` and `end_date` passed from the route, ensuring the selected dates persist after submission.
*   Add a submit button (e.g., "Filter").
*   Add a "Clear" button (e.g., a link back to `/profile` without query parameters).
*   Style the form using CSS flexbox to match the existing design aesthetic.

## Step 4: Verification
*   Test that navigating to `/profile` shows all-time data.
*   Test submitting the form with both dates to ensure data is correctly restricted.
*   Test submitting with only one date (if supported by logic) or handle missing inputs gracefully.
*   Verify that the form retains the selected dates after reloading.
