# Claude Code + OpenRouter Setup (Windows PowerShell)

## 1. Install Claude Code CLI
npm install -g @anthropic-ai/claude-code


## 2. Set Environment Variables (IMPORTANT)

# Replace with your OpenRouter API key
setx OPENROUTER_API_KEY "your-openrouter-api-key"

# Set OpenRouter as base URL
setx ANTHROPIC_BASE_URL "https://openrouter.ai/api"

# Use OpenRouter key as auth token
setx ANTHROPIC_AUTH_TOKEN "%OPENROUTER_API_KEY%"

# Must be empty (use space workaround for Windows)
setx ANTHROPIC_API_KEY " "


## 3. Restart Terminal
# Close PowerShell and open a new one


## 4. Run Claude Code
claude


## 5. First-time Setup (inside CLI)

# (A) If asked about Anthropic API key:
# Choose → "No (recommended)"  ✅

# (B) Select theme → press Enter (default is fine)

# (C) Trust folder:
# Choose → "Yes, I trust this folder"


## 6. Fix Auth Conflict (if shown)

# If you see:
# "Auth conflict: ANTHROPIC_AUTH_TOKEN and login key both set"

# Run:
/logout


## 7. Fix Credit Error (VERY IMPORTANT)

# If you see error like:
# "This request requires more credits..."

# Switch to free model:
/model openrouter/free


## 8. Test Setup

# Type any prompt:
Write a Python function for factorial

# If response comes → setup successful ✅


## ✅ Done

# Claude Code is now using:
# → OpenRouter
# → Free models (no cost)


## ⚠️ Notes (IMPORTANT)

# - Model may reset sometimes → run:
#   /model openrouter/free

# - No need to repeat setup for new projects (global config)

# - If API key is exposed → regenerate from OpenRouter

# - If switching PC → redo full setup

# - If Claude asks to use API key → ALWAYS choose "No"

# - If stuck again → check:
#   1. Terminal restarted?
#   2. Env variables set correctly?
#   3. Model switched to openrouter/free?