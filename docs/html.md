# HTML Basics

## What is HTML?
HTML is just labels (called tags) that tell the browser what content is.
Every tag has an opening <tag> and a closing </tag>.

---

## Basic Structure
Every HTML file looks like this:

```html
<!DOCTYPE html>          → tells browser this is HTML
<html lang="en">         → root, everything lives inside this
  <head>                 → invisible settings section
    <meta charset="UTF-8">   → supports all characters
    <title>My Page</title>   → text shown on browser tab
  </head>
  <body>                 → everything here shows on the page
  </body>
</html>
```

---

## Tags You Must Know

```html
<h1>Heading</h1>         → biggest heading. use only once per page
<h2>Heading</h2>         → smaller heading
<h3>Heading</h3>         → even smaller
<p>Some text</p>         → paragraph
<a href="/login">Login</a>     → clickable link. href = where it goes
<img src="photo.jpg" alt="photo">  → image. alt = text if image fails
<div>...</div>           → invisible box. used to group things together
<span>...</span>         → inline box. groups text inside a line
```

---

## Forms

```html
<form method="POST" action="/login">   → POST = send data. action = where to send it
  <input type="text" name="username" placeholder="Enter name">   → text box
  <input type="email" name="email" placeholder="Enter email">    → email box
  <input type="password" name="password" placeholder="Password"> → hides what you type
  <button type="submit">Submit</button>  → clicking this sends the form
</form>
```

---

## Lists

```html
<ul>                     → unordered list (bullet points)
  <li>Item one</li>
  <li>Item two</li>
</ul>

<ol>                     → ordered list (1, 2, 3...)
  <li>First</li>
  <li>Second</li>
</ol>
```

---

## Attributes
Attributes give extra info to a tag. They go inside the opening tag.

```html
<a href="/login">        → href is the attribute. value is /login
<img src="photo.jpg">    → src is the attribute. value is photo.jpg
<input name="email">     → name is the attribute. used to read data in backend
<div class="card">       → class is the attribute. used by CSS to style it
<div id="navbar">        → id is the attribute. unique. only one per page
```

---

## Comments
```html
<!-- This is a comment. Browser ignores it. Only you can see it. -->
```

---

## Key Rules
- Most opening tags need a closing tag (e.g., `<p>` → `</p>`). However, "void elements" like `<img>`, `<input>`, and `<br>` do not use closing tags.
- Tags can be nested inside each other
- Indentation does not affect the page. It is just for readability.
- class = used many times. id = used once per page.