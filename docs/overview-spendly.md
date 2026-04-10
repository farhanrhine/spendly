Now I can see everything clearly! Let me map out exactly what Spendly has:

```
spendly/
├── app.py                  ← Flask app (routes, logic)
├── main.py                 ← Entry point to run the app
├── database/
│   ├── __init__.py
│   └── db.py               ← Database connection & queries
├── templates/
│   ├── base.html           ← Master layout
│   ├── landing.html        ← Home page
│   ├── login.html          ← Login page
│   └── register.html       ← Register page
├── static/
│   ├── css/style.css       ← Styling
│   └── js/main.js          ← Frontend JS
└── pyproject.toml          ← Dependencies
```

This is a **Flask expense tracker with user auth (login/register) and a database**. Let me now teach you everything you need — tied directly to Spendly's actual files. 🎯

---

## 1. 🧱 HTML — What's in Spendly's Templates

### `base.html` — The Master Layout
Every page in Spendly **inherits** from this file. It holds things shared across all pages: navbar, CSS links, JS links.

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Spendly</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
  <nav><!-- navbar here --></nav>

  {% block content %}
  <!-- Each page fills this section differently -->
  {% endblock %}

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

`{% block content %}` is a **placeholder** — child pages replace it with their own content.

### `login.html` — Extends the Base
```html
<!-- login.html -->
{% extends "base.html" %}

{% block content %}
  <h1>Login to Spendly</h1>
  <form method="POST" action="/login">
    <input type="email" name="email" placeholder="Email">
    <input type="password" name="password" placeholder="Password">
    <button type="submit">Login</button>
  </form>
{% endblock %}
```

`{% extends "base.html" %}` means: "use base.html as my wrapper, and fill in the `block content` section."

The `<form method="POST" action="/login">` sends the user's data to Flask's `/login` route when they click the button.

---

## 2. 🎨 CSS — What `style.css` Does for Spendly

Your `static/css/style.css` file styles all the pages. Here's what you'll likely write for Spendly:

```css
/* Reset defaults */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
}

/* A login/register card */
.auth-card {
  width: 400px;
  margin: 80px auto;
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Inputs */
input {
  width: 100%;
  padding: 10px;
  margin: 8px 0;
  border: 1px solid #ddd;
  border-radius: 6px;
}

/* Button */
button {
  width: 100%;
  padding: 12px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #4338ca;
}
```

Then in your HTML you use: `<div class="auth-card">` to apply these styles.

---

## 3. 🐍 Flask — How `app.py` Powers Spendly

This is the brain of the project. Here's what Spendly's `app.py` likely looks like and what each part means:

```python
from flask import Flask, render_template, request, redirect, session
from database.db import get_user, create_user  # your db functions

app = Flask(__name__)
app.secret_key = "some-secret"  # needed for sessions (login state)

# Landing page
@app.route("/")
def landing():
    return render_template("landing.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]        # get form data
        password = request.form["password"]
        user = get_user(email, password)     # check database
        if user:
            session["user_id"] = user["id"] # save login state
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")     # GET request = just show the page

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        create_user(email, password)         # save to database
        return redirect("/login")
    return render_template("register.html")
```

**Key concepts here:**
- `methods=["GET", "POST"]` — GET loads the page, POST submits the form
- `request.form["email"]` — reads what the user typed in the form
- `session` — stores the logged-in user across pages (like a cookie)
- `redirect("/dashboard")` — sends user to another page after login

---

## 4. 🗄️ Database — `database/db.py`

Spendly uses a database to store users and expenses. Here's the pattern it follows:

```python
import sqlite3

def get_connection():
    conn = sqlite3.connect("spendly.db")
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    return conn

def create_user(email, password):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (email, password) VALUES (?, ?)",
        (email, password)
    )
    conn.commit()
    conn.close()

def get_user(email, password):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, password)
    ).fetchone()
    conn.close()
    return user
```

The `?` placeholders keep your queries safe from attacks. Never put variables directly in SQL strings.

---

## 5. 🗂️ Git — How to Use It on Spendly

Since you're already in the project (`main` branch), here's your daily workflow:

```bash
# See what you changed
git status

# Stage all changes
git add .

# Save a snapshot
git commit -m "Add login page styling"

# Push to GitHub
git push origin main
```

**Good Spendly commit messages:**
- `"Add register route to app.py"`
- `"Style login card in style.css"`
- `"Fix form not submitting on login page"`

---

## 🗺️ How It All Connects in Spendly

```
User visits /login
      ↓
Flask (app.py) receives request
      ↓
Renders login.html (which extends base.html)
      ↓
style.css makes it look good
      ↓
User submits form → Flask reads form data
      ↓
db.py checks the database
      ↓
User is logged in → session stores their ID
      ↓
Redirected to /dashboard
```

---
