# Implementation Plan for Profile Page (04-profile-page.md)

## Overview
- **Purpose**: Replace the `/profile` stub with a fully designed profile page displaying hardcoded static data
- **Specification Dependency**: Builds on Steps 1–3 (database setup, registration, login/logout); session must be active and user authenticated
- **Key Components**: Authentication guard, hardcoded template context, four-section UI layout (user info card, summary stats, transaction history, category breakdown)
- **Target Files**: 
  - `app.py` (replace `/profile` route with full implementation)
  - `templates/profile.html` (create new template)

---

## Current State Analysis

### Existing Route
- `GET /profile` exists in `app.py` (line ~63-64) but is a stub: `return "Profile page — coming in Step 4"`
- No template rendering
- No authentication check
- Will be completely replaced with a real view function

### Database Schema (Available for Reference)
```
users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
)

expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  amount REAL NOT NULL,
  category TEXT NOT NULL,
  date TEXT NOT NULL,
  description TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id)
)
```
- **No DB queries used in this step** — all data is hardcoded in Python context dict

### Template & Styling (Ready)
- `base.html` exists and includes:
  - Navigation bar with authentication-aware display
  - Flexbox-based responsive layout
  - CSS variables already defined in `style.css`
- `style.css` has:
  - CSS variables for colors, spacing, fonts
  - Flexbox utilities
  - Responsive breakpoints

---

## Step-by-Step Implementation

### Phase 1: Update app.py Route Handler
**Location:** `app.py` (replace line ~63-64)

#### Step 1.1: Replace /profile Route
**Current code:**
```python
@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"
```

**New implementation:**
```python
@app.route("/profile")
def profile():
    # Authentication guard
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    # Hardcoded context data
    context = {
        # User info card
        'user': {
            'name': 'John Doe',
            'email': 'john@example.com',
            'member_since': 'January 2024',
            'initials': 'JD'
        },
        
        # Summary stats
        'stats': {
            'total_spent': '$1,245.50',
            'transaction_count': 18,
            'top_category': 'Food'
        },
        
        # Transaction history (hardcoded rows)
        'transactions': [
            {'date': '2024-04-20', 'description': 'Grocery shopping', 'category': 'Food', 'amount': '$45.99'},
            {'date': '2024-04-19', 'description': 'Gas fill-up', 'category': 'Transport', 'amount': '$52.30'},
            {'date': '2024-04-18', 'description': 'Movie tickets', 'category': 'Entertainment', 'amount': '$28.00'},
            {'date': '2024-04-17', 'description': 'Electric bill', 'category': 'Bills', 'amount': '$89.50'},
            {'date': '2024-04-16', 'description': 'Pharmacy', 'category': 'Health', 'amount': '$15.75'},
        ],
        
        # Category breakdown (hardcoded totals)
        'categories': [
            {'name': 'Food', 'total': '$385.20', 'percentage': 31},
            {'name': 'Transport', 'total': '$210.80', 'percentage': 17},
            {'name': 'Bills', 'total': '$298.50', 'percentage': 24},
            {'name': 'Health', 'total': '$85.00', 'percentage': 7},
            {'name': 'Entertainment', 'total': '$140.00', 'percentage': 11},
            {'name': 'Shopping', 'total': '$95.00', 'percentage': 8},
            {'name': 'Other', 'total': '$31.00', 'percentage': 2},
        ]
    }
    
    return render_template('profile.html', **context)
```

**Key points:**
- Check `session.get('user_id')` — if falsy, redirect to login
- Build hardcoded context dict with nested structures for user, stats, transactions, categories
- Pass context to template via `**context` (unpacks dict as kwargs)
- Use realistic sample data

---

### Phase 2: Create profile.html Template
**Location:** `templates/profile.html` (new file)

#### Step 2.1: Template Structure
The template must extend `base.html` and include four sections:

**Section 1: User Info Card**
- Display avatar with initials (CSS circle with background color)
- Display name
- Display email
- Display member-since date
- Use CSS classes, no inline styles
- Example HTML structure:
  ```html
  <div class="profile-card">
    <div class="avatar">{{ user.initials }}</div>
    <h2>{{ user.name }}</h2>
    <p class="email">{{ user.email }}</p>
    <p class="member-since">Member since {{ user.member_since }}</p>
  </div>
  ```

**Section 2: Summary Stats Row**
- Three stat boxes displayed horizontally (Flexbox row)
- Stats: Total Spent, Transaction Count, Top Category
- Use CSS variables for colors and spacing
- Example:
  ```html
  <div class="stats-row">
    <div class="stat-box">
      <span class="stat-value">{{ stats.total_spent }}</span>
      <span class="stat-label">Total Spent</span>
    </div>
    <div class="stat-box">
      <span class="stat-value">{{ stats.transaction_count }}</span>
      <span class="stat-label">Transactions</span>
    </div>
    <div class="stat-box">
      <span class="stat-value">{{ stats.top_category }}</span>
      <span class="stat-label">Top Category</span>
    </div>
  </div>
  ```

**Section 3: Transaction History Table**
- Display list of recent expenses
- Columns: Date, Description, Category Badge, Amount
- Category badge must use CSS class for color (e.g., `class="badge badge-food"`)
- Use table or list; ensure responsive on mobile
- Example:
  ```html
  <table class="transactions-table">
    <thead>
      <tr>
        <th>Date</th>
        <th>Description</th>
        <th>Category</th>
        <th>Amount</th>
      </tr>
    </thead>
    <tbody>
      {% for txn in transactions %}
      <tr>
        <td>{{ txn.date }}</td>
        <td>{{ txn.description }}</td>
        <td><span class="badge badge-{{ txn.category|lower }}">{{ txn.category }}</span></td>
        <td>{{ txn.amount }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  ```

**Section 4: Category Breakdown**
- List of categories with totals and percentage bars
- Display category name, total amount, and percentage
- Use progress-bar style or simple list with visual indicator
- Example:
  ```html
  <div class="category-breakdown">
    {% for cat in categories %}
    <div class="category-row">
      <span class="category-name">{{ cat.name }}</span>
      <div class="progress-bar">
        <div class="progress-fill" style="width: {{ cat.percentage }}%"></div>
      </div>
      <span class="category-total">{{ cat.total }}</span>
    </div>
    {% endfor %}
  </div>
  ```

#### Step 2.2: CSS Considerations
- Use CSS variables from `style.css` for all colors and spacing
- No hex values in `profile.html`
- No inline styles (except `style="width: {{ cat.percentage }}%"` for progress bar percentage, which is dynamic)
- Category badges: Define CSS classes like `.badge-food`, `.badge-transport`, etc. in `style.css`
- Ensure responsive layout using Flexbox
- Mobile-first approach: stack sections vertically on small screens

---

### Phase 3: Add CSS Styling
**Location:** `static/css/style.css`

#### Step 3.1: Profile-Specific CSS Classes
Add the following CSS classes (using existing CSS variables):

```css
/* User info card */
.profile-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-lg);
  background-color: var(--color-surface);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-lg);
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: var(--spacing-md);
}

.profile-card h2 {
  margin: 0 0 var(--spacing-sm) 0;
}

.profile-card .email {
  color: var(--color-text-muted);
  margin: 0;
}

.profile-card .member-since {
  color: var(--color-text-muted);
  font-size: 14px;
  margin: var(--spacing-sm) 0 0 0;
}

/* Summary stats */
.stats-row {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  flex-wrap: wrap;
}

.stat-box {
  flex: 1;
  min-width: 150px;
  padding: var(--spacing-md);
  background-color: var(--color-surface);
  border-radius: var(--radius-md);
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.stat-label {
  display: block;
  font-size: 14px;
  color: var(--color-text-muted);
}

/* Transaction history table */
.transactions-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: var(--spacing-lg);
}

.transactions-table thead {
  background-color: var(--color-surface);
}

.transactions-table th,
.transactions-table td {
  padding: var(--spacing-md);
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.transactions-table th {
  font-weight: bold;
  color: var(--color-text-muted);
}

/* Category badges */
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.badge-food { background-color: var(--color-food, #FF6B6B); }
.badge-transport { background-color: var(--color-transport, #4ECDC4); }
.badge-bills { background-color: var(--color-bills, #FFD93D); }
.badge-health { background-color: var(--color-health, #6BCB77); }
.badge-entertainment { background-color: var(--color-entertainment, #A78BFA); }
.badge-shopping { background-color: var(--color-shopping, #F97316); }
.badge-other { background-color: var(--color-other, #64748B); }

/* Category breakdown */
.category-breakdown {
  margin-top: var(--spacing-lg);
}

.category-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--color-border);
}

.category-name {
  width: 100px;
  font-weight: 600;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: var(--color-border);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--color-primary);
  transition: width 0.3s ease;
}

.category-total {
  width: 80px;
  text-align: right;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 768px) {
  .stats-row {
    flex-direction: column;
  }

  .stat-box {
    flex: 1 1 100%;
  }

  .transactions-table {
    font-size: 14px;
  }

  .transactions-table th,
  .transactions-table td {
    padding: var(--spacing-sm);
  }
}
```

**Note:** Add CSS variables to `style.css` if not already present:
```css
:root {
  --color-food: #FF6B6B;
  --color-transport: #4ECDC4;
  --color-bills: #FFD93D;
  --color-health: #6BCB77;
  --color-entertainment: #A78BFA;
  --color-shopping: #F97316;
  --color-other: #64748B;
}
```

---

## Detailed Implementation Notes

### Authentication Guard
- Check `session.get('user_id')` at the top of the route
- If None/falsy → `redirect(url_for('login'))`
- Never render the profile template for unauthenticated users

### Hardcoded Data Structure
- All data must be Python dicts/lists (no DB queries)
- Structure mirrors what database queries would provide (for Step 5 migration)
- Use realistic sample values
- Ensure context keys match template variable names

### Template Best Practices
- Extend `base.html`: `{% extends "base.html" %}`
- Use Jinja2 filters for formatting (e.g., `{{ txn.category|lower }}`)
- Use `for` loops to iterate hardcoded lists
- No inline styles; all styling via CSS classes
- Use semantic HTML (tables for tabular data, divs for layout sections)

### CSS Variables Rule
- **CRITICAL**: No hex color values in `profile.html`
- All colors defined as CSS variables in `style.css`
- Category badges use CSS classes (`.badge-food`, etc.)
- Dynamic percentages can use inline `style="width: {{ cat.percentage }}%"` (no color involved)

---

## Verification Checklist

### Testing Steps
1. **Start the server:** `uv run app.py`
2. **Test unauthenticated access:**
   - Navigate to `http://localhost:5000/profile` without logging in
   - Verify redirect to `/login`
3. **Test authenticated access:**
   - Log in with `demo@Finlo.com` / `demo123`
   - Navigate to `/profile`
   - Verify HTTP 200 response (page loads)
4. **Verify UI sections:**
   - [ ] User info card displays name "John Doe" and email "john@example.com"
   - [ ] Avatar initials "JD" displayed in circular badge
   - [ ] Member-since date displayed
5. **Verify summary stats:**
   - [ ] Total Spent shows "$1,245.50"
   - [ ] Transaction count shows "18"
   - [ ] Top category shows "Food"
6. **Verify transaction history:**
   - [ ] Table displays at least 5 hardcoded transactions
   - [ ] Columns: Date, Description, Category, Amount
   - [ ] Category badges display with correct CSS classes (no inline colors)
   - [ ] No console errors
7. **Verify category breakdown:**
   - [ ] All 7 categories listed with totals
   - [ ] Percentage bars display correctly
   - [ ] Percentages sum to 100%
8. **Verify navbar:**
   - [ ] Logged-in username displays in header
   - [ ] Logout button/link present and functional
9. **CSS Validation:**
   - [ ] Inspect `profile.html` — no hex color values visible
   - [ ] All colors sourced from CSS variables
   - [ ] Page responsive on mobile (Flexbox layout works)
10. **No Errors:**
    - [ ] No HTTP 500 errors
    - [ ] No console JavaScript errors
    - [ ] No broken links (all use `url_for()`)

---

## Key Reminders
- **Step 4 is UI-only** — no database queries, all hardcoded
- **Step 5 will replace hardcoded data with real DB queries**
- **Focus on layout and design** — ensure template structure is correct for future DB integration
- **Session must be active** — authentication guard is required
- **CSS variables only** — no hardcoded colors in template or CSS
- **Responsive design** — test on mobile viewport
