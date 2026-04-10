---
name: Anthropic Claude MkDocs Aesthetic
description: Complete instruction set for turning a standard Material MkDocs site into a bespoke, academic "Parchment & Ink" editorial design inspired by Anthropic's Claude.
---

# 🎨 Anthropic Claude MkDocs Aesthetic

**Purpose**: When instructed to apply the "Claude Aesthetic" or "Parchment Aesthetic" to a new MkDocs project, execute the following three steps exactly to overhaul the visual design.

## Step 1: `mkdocs.yml` Overrides
Update the `theme` and `palette` block in the target `mkdocs.yml` to support the custom fonts and prepare the base theme for injection. Ensure `docs/stylesheets/extra.css` is registered.

```yaml
theme:
  name: material
  font:
    text: Inter
    code: Fira Code
  palette:
    - scheme: default
      primary: white
      accent: deep orange
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: black
      accent: deep orange
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

extra_css:
  - stylesheets/extra.css
```

## Step 2: Inject `extra.css` Configuration
Overwrite `docs/stylesheets/extra.css` with the exact variables below. This implements the "Parchment & Ink" light mode and the "Midnight Parchment" dark mode, whilst strictly enforcing `Newsreader` (headers) and `Inter` (UI elements).

```css
/* 1. Import Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap');

/* Light Mode: "Parchment & Ink" */
[data-md-color-scheme="default"] {
  --bg-base: #faf9f5;
  --text-main: #141413;
  --text-muted: #66645e;
  --accent-color: #9c462c;
  --border-color: #dcdad2;
  --border-dark: #141413;
  --bg-card: #f2f0e9;
  --bg-card-hover: #e8e6df;

  --md-default-bg-color: var(--bg-base);
  --md-default-fg-color: var(--text-main);
  --md-default-fg-color--light: var(--text-muted);
  --md-default-fg-color--lightest: var(--border-color);
  --md-primary-fg-color: var(--bg-base);
  --md-primary-bg-color: var(--text-main);
  --md-typeset-a-color: var(--accent-color);
  --md-admonition-bg-color: var(--bg-card);
}

/* Dark Mode: "Midnight Parchment" */
[data-md-color-scheme="slate"] {
  --bg-base: #1C1B19;
  --text-main: #E6E4DD;
  --text-muted: #A3A099;
  --accent-color: #D97757;
  --border-color: #3D3A36;
  --border-dark: #706B65;
  --bg-card: #282624;
  --bg-card-hover: #363330;

  --md-default-bg-color: var(--bg-base);
  --md-default-fg-color: var(--text-main);
  --md-default-fg-color--light: var(--text-muted);
  --md-default-fg-color--lightest: var(--border-color);
  --md-primary-fg-color: var(--bg-base);
  --md-primary-bg-color: var(--text-main);
  --md-typeset-a-color: var(--accent-color);
  --md-admonition-bg-color: var(--bg-card);
}

/* 3. TYPOGRAPHY - The Editorial "Claude" Feel */
body {
  font-family: 'Inter', sans-serif;
  color: var(--text-main);
  -webkit-font-smoothing: antialiased;
}

/* Base Headings -> Newsreader */
.md-typeset h1, .md-typeset h2, .md-typeset h3, 
.md-typeset h4, .md-typeset h5, .md-typeset h6 {
  font-family: 'Newsreader', Georgia, serif;
  color: var(--text-main);
  font-weight: 500;
  letter-spacing: -0.01em;
  margin-top: 2em;
  line-height: 1.3;
}

.md-typeset h1 {
  font-size: 3.5rem; 
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin-bottom: 24px;
}

.md-typeset h2 {
  font-size: 1.75rem;
  font-weight: 400;
  color: var(--text-muted);
  border-bottom: none;
}

/* 4. SIDEBAR - "Section Label" Aesthetic */
.md-nav__title,
.md-nav__item--section > .md-nav__link {
  font-family: 'Inter', sans-serif !important;
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-main) !important;
  border-bottom: 1px solid var(--border-color) !important;
  padding-bottom: 8px !important;
  margin-top: 24px !important;
}

.md-nav__link:hover, .md-nav__link--active {
  color: var(--accent-color) !important;
}

/* 5. OVERRIDES (Flat Structural lines) */
.md-header {
  box-shadow: none !important; 
  border-bottom: 1px solid var(--border-color) !important;
  background-color: var(--bg-base) !important;
  color: var(--text-main) !important;
}

.md-search__input {
  background-color: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  box-shadow: none !important;
}

/* Grounded Note Cards / Admonitions */
.md-typeset .admonition, .md-typeset details {
  box-shadow: none !important;
  border: 1px solid var(--border-color);
  background-color: var(--bg-card) !important;
  border-radius: 12px;
  border-left: 6px solid var(--accent-color) !important;
  transition: all 0.2s ease;
}

.md-typeset .admonition:hover {
  background-color: var(--bg-card-hover) !important;
  border-color: var(--border-dark);
}

/* Code Blocks */
.md-typeset pre>code {
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
}
```

## Step 3: CI/CD Pipeline Update (GitHub Actions)
If the user wants deployment set up via GitHub actions (e.g., `.github/workflows/deploy-docs.yml`), ensure they are not using generic `pip install mkdocs-material`. Instead, enforce the deployment using astral's `uv` command to correctly track local dependencies like `mkdocs-jupyter`.

```yaml
      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"

      - name: Install dependencies
        run: uv sync

      - name: Build site
        run: uv run mkdocs build
```
