# Plan: Edit Expenses

## Overview
Implementation plan for Step 08 - Edit Expenses feature. This feature adds the ability for authenticated users to edit existing expense transactions with full validation and ownership checks.

**Spec Reference**: `.claude/specs/08-edit-expenses.md`

---

## Architecture & Approach

### Template Strategy: Reuse `add_expense.html`
- Modify `add_expense.html` to accept optional `expense` object (for edit mode)
- Use conditional rendering to show "Add Expense" vs "Edit Expense" title
- Form `action` will use `url_for()` with dynamic route:
  - Add mode: `url_for('add_expense_post')`
  - Edit mode: `url_for('edit_expense_post', id=expense.id)`
- This avoids duplicating 95% of identical markup

### Database Layer
- Add `get_expense_by_id(user_id, expense_id)` to `queries.py` — fetches with ownership check
- Add `update_expense(user_id, expense_id, ...)` to `queries.py` — validates and updates with ownership check

### Route Handlers
- `GET /expenses/<id>/edit` — fetch expense, ownership check, render form
- `POST /expenses/<id>/edit` — CSRF validation, ownership check, validate inputs, update, redirect

---

## Implementation Tasks

### Phase 1: Database Layer (`database/queries.py`)

#### Task 1.1: Add `get_expense_by_id()`
```python
def get_expense_by_id(user_id, expense_id):
    """
    Fetch a single expense by ID with ownership validation.
    
    Args:
        user_id: Authenticated user's ID
        expense_id: Expense ID to fetch
    
    Returns:
        dict with keys: id, user_id, amount, category, date, description, created_at
        OR None if not found or user doesn't own it
    """
```

**Implementation notes:**
- Query: `SELECT id, amount, category, date, description FROM expenses WHERE id = ? AND user_id = ?`
- Return as dict (use `conn.row_factory = sqlite3.Row`)
- Closes connection in finally block
- Returns None if expense doesn't exist or user_id doesn't match

#### Task 1.2: Add `update_expense()`
```python
def update_expense(user_id, expense_id, amount, category, date, description=None):
    """
    Update an existing expense with validation and ownership check.
    
    Args:
        user_id: Authenticated user's ID (for ownership check)
        expense_id: Expense ID to update
        amount: New amount (must be positive)
        category: New category (must be in allowed list)
        date: New date (YYYY-MM-DD format)
        description: New description (optional)
    
    Returns:
        int: The updated expense_id
    
    Raises:
        ValueError: If validation fails or user doesn't own the expense
    """
```

**Implementation notes:**
- Validate identically to `create_expense()`: amount > 0, category in list, date valid
- Check ownership: verify `(expense_id, user_id)` pair exists in database
- If ownership check fails, raise `ValueError("Expense not found or access denied")`
- Query: `UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? WHERE id = ? AND user_id = ?`
- Return expense_id on success

---

### Phase 2: Template Changes (`templates/add_expense.html`)

#### Task 2.1: Modify form structure for dual-mode rendering
```html
<!-- Top of file: adjust based on whether expense exists -->
<h1>{% if expense %}Edit Expense{% else %}Add Expense{% endif %}</h1>
```

**Changes needed:**
1. Add optional `expense` variable in template context (defaults to None)
2. Pre-populate form fields if `expense` exists:
   - `amount`: `value="{{ expense.amount }}"`
   - `category`: select option `selected` if matches `expense.category`
   - `date`: `value="{{ expense.date }}"`
   - `description`: textarea content = `expense.description or ''`
3. Form action URL:
   ```html
   <form method="POST" action="{% if expense %}{{ url_for('edit_expense_post', id=expense.id) }}{% else %}{{ url_for('add_expense_post') }}{% endif %}">
   ```
4. Submit button text:
   ```html
   <button type="submit">{% if expense %}Update Expense{% else %}Add Expense{% endif %}</button>
   ```
5. Keep CSRF token field unchanged

#### Task 2.2: Verify styling consistency
- Form layout already uses Flexbox in `style.css`
- Inputs already styled with CSS variables
- No additional CSS needed (reuse existing styles)

---

### Phase 3: Route Handlers (`app.py`)

#### Task 3.1: Implement `GET /expenses/<id>/edit`
```python
@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    """
    Display the expense edit form pre-populated with current data.
    Only accessible to authenticated users who own the expense.
    """
    # Authentication guard
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    # Fetch expense with ownership check
    expense = get_expense_by_id(user_id, id)
    if not expense:
        abort(404)
    
    # Ensure CSRF token exists
    import secrets
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    csrf_token = session.get('csrf_token')
    
    # Categories list
    categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
    
    # Render form with pre-populated data
    return render_template('add_expense.html',
                         expense=expense,
                         categories=categories,
                         csrf_token=csrf_token)
```

**Implementation notes:**
- Import `abort` from Flask at top of file
- Use `get_expense_by_id(user_id, id)` helper from queries
- Return 404 if expense not found or not owned by user
- Pre-populate CSRF token (same as add_expense_post)

#### Task 3.2: Implement `POST /expenses/<id>/edit`
```python
@app.route("/expenses/<int:id>/edit", methods=["POST"])
def edit_expense_post(id):
    """
    Handle expense edit form submission.
    Validates inputs, updates expense, and redirects to profile.
    """
    # Authentication guard
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    # CSRF token validation
    csrf_token = request.form.get('csrf_token', '')
    session_token = session.get('csrf_token', '')
    if not csrf_token or csrf_token != session_token:
        expense = get_expense_by_id(user_id, id)
        if not expense:
            abort(404)
        categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
        return render_template('add_expense.html',
                             expense=expense,
                             categories=categories,
                             error='Security token expired. Please refresh and try again.')
    
    # Extract form data
    amount = request.form.get('amount', '').strip()
    category = request.form.get('category', '').strip()
    date = request.form.get('date', '').strip()
    description = request.form.get('description', '').strip()
    
    # Categories list for re-rendering on error
    categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Other']
    
    # Validate amount is convertible to float
    try:
        float(amount)
    except ValueError:
        expense = get_expense_by_id(user_id, id)
        if not expense:
            abort(404)
        return render_template('add_expense.html',
                             expense=expense,
                             categories=categories,
                             error='Amount must be a valid number',
                             amount=amount,
                             category=category,
                             date=date,
                             description=description)
    
    # Try to update the expense
    try:
        expense_id = update_expense(user_id, id, amount, category, date, description)
        return redirect(url_for('profile'))
    except ValueError as e:
        expense = get_expense_by_id(user_id, id)
        if not expense:
            abort(404)
        return render_template('add_expense.html',
                             expense=expense,
                             categories=categories,
                             error=str(e),
                             amount=amount,
                             category=category,
                             date=date,
                             description=description)
```

**Implementation notes:**
- Ownership check happens implicitly through `get_expense_by_id()` and `update_expense()`
- If expense doesn't exist or user doesn't own it, abort 404
- CSRF validation identical to add_expense_post
- Error handling preserves form values
- Redirect to profile on success

---

## Testing Checklist

### Manual Testing (in browser)
- [ ] Add an expense first (use Step 7 feature)
- [ ] Click edit link on an expense in profile page (not yet implemented, but routes work)
- [ ] Verify form pre-populates with correct data
- [ ] Edit amount, change category, modify description, update date
- [ ] Submit form and verify redirect to profile
- [ ] Verify expense updated in the database
- [ ] Try editing with invalid data (negative amount, invalid date) — verify error message
- [ ] Try accessing `/expenses/<id>/edit` for an expense not owned by user — verify 404
- [ ] Try accessing with CSRF token mismatch — verify error message
- [ ] Test unauthenticated access (logout, then try edit) — verify redirect to login

### Security Testing
- [ ] Verify user cannot edit another user's expense (404 on access)
- [ ] Verify CSRF protection works (tamper with token)
- [ ] Verify date validation (try past dates before 2000, future dates)
- [ ] Verify amount validation (try zero, negative, non-numeric)
- [ ] Verify category validation (try invalid category from form manipulation)

---

## Files Summary

| File | Changes | Status |
|------|---------|--------|
| `database/queries.py` | Add `get_expense_by_id()`, `update_expense()` | To create |
| `templates/add_expense.html` | Add conditional rendering for edit mode, pre-populate fields | To modify |
| `app.py` | Implement `GET /expenses/<id>/edit`, `POST /expenses/<id>/edit`, import `abort` | To modify |

---

## Commit Strategy

**Phase 1 Commit**: Database layer
```
git add database/queries.py
git commit -m "Add get_expense_by_id and update_expense query helpers

- get_expense_by_id: Fetch expense with ownership validation
- update_expense: Update expense with validation and ownership check"
```

**Phase 2 Commit**: Template changes
```
git add templates/add_expense.html
git commit -m "Modify add_expense form for dual-mode (add/edit)

- Add conditional rendering for edit vs add titles
- Pre-populate form fields when expense provided
- Dynamic form action URL using url_for()"
```

**Phase 3 Commit**: Routes
```
git add app.py
git commit -m "Implement GET/POST routes for edit expense feature

- GET /expenses/<id>/edit: Display pre-populated form
- POST /expenses/<id>/edit: Validate and update expense
- Ownership and CSRF validation on both routes"
```

---

## Notes

- **Reusing template**: Simplifies maintenance and reduces bugs (single source of truth for form markup)
- **Ownership checks**: Every step validates user_id to prevent cross-user access
- **Validation parity**: Update validation matches create validation exactly (same categories, date bounds, amount rules)
- **Error handling**: Preserves user input on validation failure (better UX)
- **No delete yet**: Step 9 will handle delete operations
