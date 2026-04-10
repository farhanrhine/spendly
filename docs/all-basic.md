**Recommended Order:** HTML & CSS → Flask → Git & GitHub for  complete beginner

This way, by the time you build a Flask web app, you'll already understand the frontend side, and Git will help you save your progress as you go.

---

Let's start with **HTML & CSS** since it's the most visual and beginner-friendly.

---

## 🌐 HTML — The Skeleton of a Webpage

HTML (HyperText Markup Language) uses **tags** to structure content. Think of it like labeling parts of a document.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My First Page</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
    <p>This is a paragraph.</p>
    <a href="https://google.com">Click me</a>
  </body>
</html>
```

**Key tags to know:**
- `<h1>` to `<h6>` — Headings (h1 is biggest)
- `<p>` — Paragraph
- `<a href="...">` — Link
- `<img src="...">` — Image
- `<div>` — A generic container (used a lot!)
- `<ul>` / `<li>` — Bullet list

---

## 🎨 CSS — The Styling Layer

CSS (Cascading Style Sheets) makes your HTML look good. You can write it in a `<style>` tag or a separate `.css` file.

```html
<style>
  h1 {
    color: blue;
    font-size: 36px;
  }

  p {
    color: gray;
    font-family: Arial, sans-serif;
  }

  .card {
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 8px;
  }
</style>

<h1>Styled Heading</h1>
<p>Styled paragraph</p>
<div class="card">I'm a card!</div>
```

**Key CSS concepts:**
- **Selectors** — target elements (`h1`, `.classname`, `#id`)
- **Properties** — what you change (`color`, `font-size`, `margin`, `padding`)
- **Box model** — every element is a box with `margin → border → padding → content`

---

## 🐍 Flask — Python Web Framework

Flask lets you build websites using Python. It handles the "backend" — the logic, data, and routing.

**Installation:**
```bash
pip install flask
```

**Your first Flask app:**
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")          # This is the URL path
def home():
    return "<h1>Hello from Flask!</h1>"

@app.route("/about")
def about():
    return "<p>This is the about page.</p>"

if __name__ == "__main__":
    app.run(debug=True)
```

Run it with `python app.py` and visit `http://localhost:5000` in your browser.

**Connecting Flask with HTML (Templates):**

Flask uses a folder called `templates/` to store HTML files.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", name="Farhan")
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
  <body>
    <h1>Hello, {{ name }}!</h1>  <!-- Flask fills this in -->
  </body>
</html>
```

The `{{ name }}` is **Jinja2 templating** — Flask's way of injecting Python data into HTML.

---

## 🗂️ Git & GitHub — Saving & Sharing Your Code

**Git** tracks changes to your code locally. **GitHub** is where you store it online.

**One-time setup:**
```bash
git config --global user.name "Your Name"
git config --global user.email "you@email.com"
```

**The everyday workflow:**
```bash
# 1. Start tracking a project
git init

# 2. See what's changed
git status

# 3. Stage your changes (prepare to save)
git add .

# 4. Save a snapshot with a message
git commit -m "Added home page"

# 5. Push to GitHub
git push origin main
```

**Connecting to GitHub:**
```bash
git remote add origin https://github.com/yourname/your-repo.git
git push -u origin main
```

**The golden rule of commits:** commit often, with clear messages like `"Added login page"` or `"Fixed navbar bug"`.

---

## 🗺️ How They All Connect in Your Project

```
Your Project/
│
├── app.py              ← Flask (Python backend)
├── templates/
│   └── index.html      ← HTML structure
├── static/
│   └── style.css       ← CSS styling
└── .git/               ← Git tracking your progress
```

Flask serves the HTML, HTML links to CSS, and Git keeps everything safe.

---
