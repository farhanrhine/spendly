# 📚 Spendly — Learning Roadmap

> **Goal:** Learn just enough to build Spendly with Claude Code, while understanding every line of code you review.

---

## ⚡ The Rules (Read These First)

- ✅ Learn one topic at a time — finish Phase 1 before touching Phase 2
- ✅ After Claude Code generates code, review every line before moving on
- ✅ If you don't understand a line, ask: *"Explain this line by line like I'm a beginner"*
- ❌ Don't jump ahead to CSS Grid until Flexbox is solid
- ❌ Don't start building until you've read the Claude Code sheets

---

## 🗺️ The 3 Phases

```
Phase 1 → Understand the tools
Phase 2 → Build Spendly features
Phase 3 → Polish the UI
```

---

## Phase 1 — Before You Write Any Code

Read these **in order**. Each one takes ~10–15 min.

| # | Sheet | URL | What to focus on |
|---|-------|-----|-----------------|
| 1 | Claude Code Essentials | https://www.devsheets.io/sheets/claude-code | CLI commands you'll type daily |
| 2 | Claude Code Slash Commands | https://www.devsheets.io/sheets/claude-code-slash-commands | Keep open while working |
| 3 | AI Workflow | https://www.devsheets.io/sheets/ai-workflow | "Break Down Features" + "Don't Understand AI's Code" sections |
| 4 | Python Fundamentals | https://www.devsheets.io/sheets/python-fundamentals | Dicts, functions, exception handling — used in `db.py` & `app.py` |

**✅ Done when:** You can run Claude Code in your terminal and understand what it's doing.

---

## Phase 2 — Building Spendly

Read these **as you build each feature**. Don't read ahead.

| # | Sheet | URL | When to read it |
|---|-------|-----|----------------|
| 5 | Flask | https://www.devsheets.io/sheets/flask | Before touching `app.py` — focus on Routing + Auth sections |
| 6 | HTML5 Tags | https://www.devsheets.io/sheets/html5-tags | Before editing any `.html` file in `templates/` |
| 7 | Git | https://www.devsheets.io/sheets/git | Before your first commit — run `git add . && git commit` after every feature |
| 8 | Flexbox | https://www.devsheets.io/sheets/flexbox | When styling `login.html`, `register.html` — centering cards, navbars |

**✅ Done when:** Login, Register, and Landing pages work end-to-end.

---

## Phase 3 — Polish the UI

Read this **only after Phase 2 is complete**.

| # | Sheet | URL | What to focus on |
|---|-------|-----|-----------------|
| 9 | CSS Grid | https://www.devsheets.io/sheets/css-grid | Expense dashboard layout, tables, multi-column layouts |

**✅ Done when:** The dashboard looks clean and structured.

---

## 🔁 Daily Workflow (Follow This Every Session)

```
1. Open Claude Code in your terminal
2. Pick ONE small feature to build (20–30 min max)
3. Ask Claude Code to implement it
4. Read every line of generated code
5. If confused → ask "Explain this line by line"
6. Test it manually in the browser
7. git add . && git commit -m "what you built"
8. Close the laptop. Done for the session.
```

---

## 🗂️ Spendly File Map (Quick Reference)

```
spendly/
├── app.py              ← Flask routes (learn: Flask sheet)
├── main.py             ← Run the app with: python main.py
├── database/
│   └── db.py           ← SQL queries (learn: Python Fundamentals)
├── templates/
│   ├── base.html       ← Master layout (all pages extend this)
│   ├── landing.html    ← Home page
│   ├── login.html      ← Login form
│   └── register.html   ← Register form
├── static/
│   ├── css/style.css   ← Styling (learn: Flexbox → CSS Grid)
│   └── js/main.js      ← Frontend JS (later)
└── pyproject.toml      ← Project dependencies
```

---

## 🚨 When You're Stuck

| Problem | What to do |
|---------|-----------|
| Don't understand a line of code | Ask: *"Explain this line by line like I'm a beginner"* |
| Claude Code keeps breaking things | Ask for changes to **one specific file** at a time |
| A feature feels too big | Break it into smaller steps (20–30 min each) |
| Not sure what to commit | One commit per working feature |

---

## 📌 Commit Message Guide

```bash
# Good commit messages for Spendly
git commit -m "Add login route to app.py"
git commit -m "Style login card with flexbox"
git commit -m "Add create_user function to db.py"
git commit -m "Fix form not submitting on register page"
```

---

*You own every line of code in this project. When in doubt, slow down — quality compounds.*


## 🌐 Hosting & Deployment Concepts

- GitHub = code hosting (shows .html files as code text)

### GitHub Pages
- **What it is:** Free static web hosting built into GitHub
- **URL format:** `https://username.github.io/repository-name/`
- **Works with:** HTML, CSS, JavaScript (static files only)
- **Use case:** Primers, documentation, portfolios, landing pages
- **Cannot run:** Python, databases, or backend code
- **learn more here:** https://pages.github.com/

### For Full-Stack / Python / ML Projects
| Platform | Best For | Python Support | Cost |
|----------|----------|---|---|
| **Hugging Face Spaces** | ML demos, interactive notebooks | ✅ Yes | Free |
| **Streamlit Cloud** | ML dashboards & interactive apps | ✅ Yes | Free |
| **Render** | Flask, FastAPI, Django apps | ✅ Yes | Free tier available |
| **Railway** | Full-stack applications | ✅ Yes | Free tier available |

### Key Takeaways
- **Static hosting (GitHub Pages)** = great for documentation and learning resources
- **Dynamic hosting** = needed when your app uses databases, Python backend, or ML models
- This project uses **Flask (Python backend)**, so it will eventually need full-stack hosting like Render or Railway