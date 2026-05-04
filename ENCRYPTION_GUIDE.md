# Encryption Guide for Private Folders

This guide explains how to encrypt sensitive folders in your Git repositories so they're pushed to GitHub but remain private and unreadable without your encryption key.

**Status**: Applied to `docs/` folder in this project.

---

## ⚠️ CRITICAL SECURITY WARNING

**NEVER include your actual encryption key in this guide or any public file!**
- Your `.encryption.key` must NEVER be committed to GitHub
- Your `.encryption.key` must NEVER be shared in documentation
- Always use PLACEHOLDER examples (like `YOUR-SECRET-KEY-HERE`) in guides
- Store your real key in a **password manager** (1Password, Bitwarden, LastPass)

---

## Overview

This project uses **Fernet symmetric encryption** (from Python's `cryptography` library) to protect the `docs/` folder. The entire folder is encrypted into a single `docs.tar.gz.encrypted` file, making it impossible for anyone without the key to see:
- Filenames
- Folder structure
- File contents

---

## What Was Set Up

| File | Purpose |
|------|---------|
| `.encryption.key` | Your private encryption key (NEVER committed to GitHub) |
| `encrypt_docs.py` | Script to encrypt/decrypt individual files |
| `archive_docs.py` | Script to create/extract encrypted archives |
| `docs.tar.gz.encrypted` | Encrypted archive on GitHub (visible but unreadable) |
| `.gitignore` | Updated to prevent key from being committed |

---

## Step-by-Step Setup (for this project)

### 1. Install Cryptography Package
```bash
uv add cryptography
```

### 2. Generate Encryption Key
```bash
python encrypt_docs.py genkey
```

**Output**:
```
✅ Encryption key generated: C:\Users\yourname\yourproject\.encryption.key
🔑 Key: YOUR-SECRET-KEY-HERE-DO-NOT-SHARE (64 character string)
```

⚠️ **SAVE THIS KEY SAFELY** - You'll need it to decrypt on other machines.

### 3. Create `.gitattributes` (optional, for git-crypt compatibility)
```bash
echo "docs/ filter=git-crypt diff=git-crypt" > .gitattributes
```

### 4. Encrypt the Folder
```bash
python archive_docs.py create
```

**Output**:
```
✅ Encrypted archive created: docs.tar.gz.encrypted
```

### 5. Commit and Push
```bash
git add docs.tar.gz.encrypted .encryption.key (DON'T COMMIT THE KEY!)
git add encrypt_docs.py archive_docs.py .gitignore .gitattributes
git commit -m "Add encryption setup for sensitive folders"
git push origin main
```

---

## How to Use After Setup

### Extract and Work Locally
```bash
# Extract and decrypt docs/
uv run archive_docs.py extract

# Edit files as needed in docs/

# Re-encrypt when done
uv run archive_docs.py create

# Push encrypted archive to GitHub
git add docs.tar.gz.encrypted
git commit -m "Update encrypted docs"
git push
```

### On Another Machine (with your key)
```bash
# Clone repo
git clone https://github.com/yourname/yourrepo.git
cd yourrepo

# Copy your .encryption.key file to root directory

# Extract encrypted archive
uv run archive_docs.py extract

# Now you can work with docs/ normally
```

### Re-encrypt Before Pushing
**Important**: Never commit decrypted `docs/` folder. Always encrypt before pushing:

```bash
# After making changes to docs/
uv run archive_docs.py create

# Verify you have only the encrypted file
ls docs.tar.gz.encrypted
# Should show: docs.tar.gz.encrypted (NOT the docs/ folder)

# Push
git add docs.tar.gz.encrypted
git commit -m "Update encrypted docs"
git push
```

---

## Simple Daily Workflow

### **5-Step Process Every Time You Edit:**

```bash
# 1️⃣ Extract (decrypt)
uv run archive_docs.py extract

# 2️⃣ Edit files
# Open and edit docs/PLAN/note.md (or any file)

# 3️⃣ Save changes
# Just save normally in your editor (Ctrl+S)

# 4️⃣ Re-encrypt
uv run archive_docs.py create

# 5️⃣ Push to GitHub
git add docs.tar.gz.encrypted
git commit -m "Update docs"
git push
```

---

## Common Changes: What Happens?

### **Case 1: Delete a File from docs/**
```bash
# 1. Extract
uv run archive_docs.py extract

# 2. Delete the file
rm docs/PLAN/note.md

# 3. Re-encrypt (captures deletion)
uv run archive_docs.py create

# 4. Push
git add docs.tar.gz.encrypted
git commit -m "Remove old note.md"
git push
# ✅ Works perfectly!
```

### **Case 2: Add a New File to docs/**
```bash
# 1. Extract
uv run archive_docs.py extract

# 2. Create new file
echo "New content" > docs/PLAN/new-plan.md

# 3. Re-encrypt (captures new file)
uv run archive_docs.py create

# 4. Push
git add docs.tar.gz.encrypted
git commit -m "Add new-plan.md"
git push
# ✅ Works perfectly!
```

### **Case 3: Edit Existing File (Multiple Changes)**
```bash
# 1. Extract
uv run archive_docs.py extract

# 2. Make multiple changes
# - Delete: docs/pdf/old.pdf
# - Edit: docs/basic/flask.md
# - Add: docs/idea/new-concept.md

# 3. Re-encrypt (captures all changes)
uv run archive_docs.py create

# 4. Push
git add docs.tar.gz.encrypted
git commit -m "Update docs: delete old PDF, edit flask guide, add new concept"
git push
# ✅ All changes encrypted and pushed!
```

### **⚠️ What NOT to Do:**
```bash
# ❌ DON'T delete docs/ folder manually
rm -rf docs/
uv run archive_docs.py create
# ERROR: docs/ directory not found!

# ✅ CORRECT: Always extract first
uv run archive_docs.py extract
# Now you can delete/edit/add files
```

---

## Recovery: Laptop Broken?

**Don't worry! Your docs are safe on GitHub!**

### **Recovery Steps (New Laptop):**

```bash
# 1. Clone repo
git clone https://github.com/yourname/finlo.git
cd finlo

# 2. Copy your encryption key
# From password manager or backup:
cp /backup/location/.encryption.key .

# 3. Extract and decrypt
uv run archive_docs.py extract

# 4. Done! ✅ Full docs/ folder is restored
ls docs/
# All your files are back!
```

### **Why This Works:**

| Backup Location | Status | Contains |
|-----------------|--------|----------|
| GitHub (docs.tar.gz.encrypted) | ✅ Public, Safe | 100% of your docs (encrypted) |
| Your Encryption Key | ✅ Secure backup | Decryption key |
| Combined | ✅ Unbreakable | Complete recovery possible |

**If you have both, you can recover everything!** 🔒

---

## Key Backup Checklist

### **Store Your Key In:**
- ✅ Password Manager (1Password, Bitwarden, LastPass) - REQUIRED
- ✅ USB Drive (encrypted, in safe location) - RECOMMENDED
- ✅ Cloud Backup (Google Drive, OneDrive, encrypted) - OPTIONAL

### **Never Store Key In:**
- ❌ GitHub or any Git repo
- ❌ Plain text files
- ❌ Email
- ❌ Slack or Discord
- ❌ Unencrypted cloud storage

---

## How to Apply This to Other Projects

### Quick Start for New Projects
Copy these files to your new project:
- `encrypt_docs.py`
- `archive_docs.py`
- `.gitattributes`

Then follow steps 1-5 above:

```bash
# 1. Add cryptography
uv add cryptography

# 2. Generate your encryption key (use same key for all projects if you want)
uv run encrypt_docs.py genkey

# 3. Create .gitattributes (optional)
echo "sensitive_folder/ filter=git-crypt diff=git-crypt" > .gitattributes

# 4. Encrypt the folder
# Edit archive_docs.py line 11: change DOCS_DIR to your folder name
uv run archive_docs.py create

# 5. Commit and push
git add *.tar.gz.encrypted encrypt_docs.py archive_docs.py .gitattributes .gitignore
git commit -m "Add encryption for sensitive folder"
git push
```

### Encrypt Multiple Folders
For multiple sensitive folders, you can:

**Option A**: Create separate archives
```bash
# Create archive_secrets.py, archive_config.py, etc.
# Each handles a different folder
```

**Option B**: Encrypt all into one archive
```bash
# Modify archive_docs.py to include multiple directories:
# tar.add(DOCS_DIR, arcname="docs")
# tar.add(SECRETS_DIR, arcname="secrets")
# tar.add(CONFIG_DIR, arcname="config")
```

---

## Security Best Practices

### ✅ DO:
- Save your `.encryption.key` in a **password manager** (1Password, Bitwarden, LastPass)
- Use different keys for different projects (optional but recommended)
- Store backup keys in a **safe location**
- Always encrypt before pushing to GitHub
- Never commit `.encryption.key`
- Share the key **only with trusted team members** (via secure channel, not Git)

### ❌ DON'T:
- Hardcode keys in config files
- Share keys via email or Slack
- Store keys in `.env` or environment variables in Git
- Leave decrypted folders in working directory
- Push decrypted `docs/` to GitHub

---

## Files Reference

### `encrypt_docs.py`
**Purpose**: Encrypt/decrypt individual files in a folder

**Usage**:
```bash
uv run encrypt_docs.py genkey      # Generate new key
uv run encrypt_docs.py encrypt     # Encrypt all files in docs/
uv run encrypt_docs.py decrypt     # Decrypt all files in docs/
```

**Output**: Files encrypted in-place (decrypted docs appear normal locally)

---

### `archive_docs.py`
**Purpose**: Create/extract encrypted tar.gz archive (recommended approach)

**Usage**:
```bash
uv run archive_docs.py create      # Create docs.tar.gz.encrypted
uv run archive_docs.py extract     # Extract and decrypt to docs/
```

**Advantage**: Single file, hides all filenames and structure

---

## What Gets Encrypted?

### Currently Encrypted (`docs/` folder):
```
docs/
├── basic/
│   ├── all-basic.md
│   ├── css.md
│   ├── flask.md
│   └── ...
├── idea/
│   ├── Aesthetic.md
│   ├── DESIGN_SYSTEM.md
│   └── ...
├── PLAN/
│   └── ...
└── pdf/
    └── ...
```

**All 20 files encrypted** into `docs.tar.gz.encrypted`

---

## Troubleshooting

### "Key file not found"
```bash
# Solution: Generate key first
uv run encrypt_docs.py genkey
```

### "Decryption failed"
```bash
# Make sure you're using the correct .encryption.key file
# Verify key matches the one used to encrypt
cat .encryption.key
```

### "docs.tar.gz.encrypted not found"
```bash
# Create archive first
uv run archive_docs.py create
```

### "docs/ folder still visible on GitHub"
```bash
# Check .gitignore includes docs/
cat .gitignore | grep docs

# Force remove from Git tracking
git rm -r --cached docs/
git commit -m "Remove decrypted docs from Git"
git push
```

---

## Example Workflow

```bash
# 1. Clone repo with encryption
git clone https://github.com/yourname/yourrepo.git
cd yourrepo
cp /secure/location/.encryption.key .

# 2. Extract docs
uv run archive_docs.py extract

# 3. Edit files in docs/
nano docs/basic/flask.md

# 4. Re-encrypt
uv run archive_docs.py create

# 5. Commit encrypted version
git add docs.tar.gz.encrypted
git commit -m "Update documentation"
git push

# 6. Clean up (keep docs/ for local work or remove)
# Optional: rm -rf docs/  (docs.tar.gz.encrypted is on GitHub)
```

---

## Next Steps

For this project:
1. ✅ Encryption setup complete
2. ✅ Key generated and saved (check with `cat .encryption.key`)
3. ✅ Pushed to GitHub as `docs.tar.gz.encrypted`
4. ✅ Follow the **Simple Daily Workflow** above for any edits
5. ⏭️ **For collaborators**: Share `.encryption.key` via password manager
6. ⏭️ **Backup**: Store key in multiple secure locations

---

## FAQ

**Q: Can I share my encryption key with team members?**
A: Yes! Share the key via 1Password, Bitwarden, or a password manager. Never share via email/Slack/Git.

**Q: What if I lose my encryption key?**
A: If you lose the key, the `docs.tar.gz.encrypted` file becomes unrecoverable. Keep a backup in a secure location.

**Q: Can I use the same key for multiple projects?**
A: Yes, you can reuse keys across projects. Store it in your password manager.

**Q: How do I know the archive is encrypted correctly?**
A: Open `docs.tar.gz.encrypted` in a text editor. You should see random binary characters, not readable text.

**Q: Can I encrypt other folders the same way?**
A: Yes! Copy `archive_docs.py`, change the folder name, and follow the steps above.

**Q: Is this as secure as git-crypt?**
A: Yes, Fernet uses AES-128 encryption (same security level). The difference: Archives hide the structure completely.

---

## References

- [Cryptography Documentation](https://cryptography.io/)
- [Fernet (symmetric encryption)](https://cryptography.io/en/latest/fernet/)
- [Python tarfile Documentation](https://docs.python.org/3/library/tarfile.html)

---

**Last Updated**: May 4, 2026
**Setup by**: Claude Code
**Project**: Finlo
