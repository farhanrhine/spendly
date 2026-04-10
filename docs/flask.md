# Flask Basics

## What is Flask?
Flask is a Python web framework. It listens for browser requests
and runs a Python function in response.

---

## Installation

```python
pip install flask
```

---

## Minimal Flask App

```python
from flask import Flask

app = Flask(__name__)        → creates the Flask app

@app.route("/")              → when someone visits /, run this function
def home():
    return "Hello World"     → sends this text back to the browser

if __name__ == "__main__":
    app.run(debug=True)      → starts the server. debug=True auto-reloads on changes
```

---

## Common Flask Imports

```python
from flask import (
    Flask,            → creates the app
    render_template,  → loads an HTML file and returns it
    request,          → reads data sent from a form
    redirect,         → sends user to a different URL
    session           → stores data across requests (like who is logged in)
)
```

---

## Routes

```python
@app.route("/")              → matches the URL /
@app.route("/login")         → matches the URL /login
@app.route("/register")      → matches the URL /register

@app.route("/user/<int:id>") → dynamic route. id is passed as argument
def get_user(id):
    return f"User {id}"
```

---

## GET vs POST

```python
GET   → user just visits the URL. no data is sent.
POST  → user submitted a form. data is sent to Flask.

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":     → form was submitted
        pass
    return render_template("login.html")  → just visiting the page
```

---

## Reading Form Data

```python
email = request.form["email"]        → reads input with name="email"
password = request.form["password"]  → reads input with name="password"

→ name in request.form must match name= attribute in the HTML input
```

---

## render_template

```python
return render_template("login.html")              → loads templates/login.html
return render_template("login.html", name="Alex") → passes data to the HTML

→ in the HTML you access it with {{ name }}
```

---

## redirect

```python
return redirect("/dashboard")    → sends browser to /dashboard
return redirect("/login")        → sends browser to /login

→ use after a successful form submission, not to show a page
```

---

## render_template vs redirect

```python
render_template   → show an HTML page
redirect          → send user to another URL

login failed  → render_template("login.html", error="Wrong password")
login success → redirect("/dashboard")
```

---

## session — remembering the logged in user

```python
session["user_id"] = user["id"]      → save after login
session["user_id"]                   → read it anywhere in the app
"user_id" in session                 → check if user is logged in
session.clear()                      → log the user out

→ session needs a secret key to work:
app.secret_key = "your-secret-key"
```

---

## Protecting a Route

```python
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:     → not logged in
        return redirect("/login")    → send them away
    return render_template("dashboard.html")
```

---

## Templates — Jinja2

Flask uses Jinja2 to add Python logic inside HTML files.

```python
{{ variable }}           → print a value from Python
{{ name }}               → prints whatever name= was passed in render_template

{% if user %}            → if statement
  <p>Welcome</p>
{% endif %}

{% for item in items %}  → loop
  <p>{{ item }}</p>
{% endfor %}

{% extends "base.html" %}       → inherit layout from base.html
{% block content %}             → slot that child pages fill in
{% endblock %}
```

---

## url_for

```python
url_for("login")                          → generates the URL for the login() function
url_for("static", filename="css/style.css") → correct path to a static file

→ always use url_for instead of hardcoding paths
```

---

## Project Structure Flask Expects

```text
project/
├── app.py                → your Flask app
├── templates/            → all HTML files go here
│   ├── base.html
│   └── login.html
└── static/               → all CSS, JS, images go here
    └── css/
        └── style.css
```

---

## Running the App

```python
python app.py             → starts the server
python main.py            → same if your entry point is main.py

→ visit http://localhost:5000 in the browser
```

---

## Key Rules
- @app.route() always goes directly above the function it decorates
- function name must be unique across all routes
- templates folder must be named exactly templates
- static folder must be named exactly static
- always set app.secret_key before using session
- debug=True is for development only. never use in production