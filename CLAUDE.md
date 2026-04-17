# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the dev server (port 5001)
python3 app.py

# Run tests
pytest

# Install dependencies
pip install -r requirements.txt
```

The venv is at `venv/` — activate with `source venv/bin/activate` before running commands if packages aren't on the system Python.

## Architecture

This is a **Flask** app (`app.py`) with no database yet. All routes currently return either a rendered template or a placeholder string. Backend logic (auth, expenses, DB) is stubbed out and will be added incrementally by students.

**Route → template mapping:**

| Route | Template | Status |
|---|---|---|
| `/` | `landing.html` | Done |
| `/register` | `register.html` | UI done, no POST handler |
| `/login` | `login.html` | UI done, no POST handler |
| `/terms` | `terms.html` | Done |
| `/privacy` | `privacy.html` | Done |
| `/logout`, `/profile`, `/expenses/*` | — | Placeholder strings |

**Templates** all extend `base.html`, which provides the navbar, footer, and shared CSS/JS includes. The footer contains Terms and Privacy links.

**CSS split:**
- `static/css/style.css` — global styles, design tokens (CSS variables), all non-landing pages
- `static/css/landing.css` — landing-page-only overrides; loaded via `{% block head %}` in `landing.html`

**Design tokens** are defined as CSS variables in `:root` inside `style.css`: `--ink`, `--paper`, `--accent` (dark green `#1a472a`), `--accent-2` (amber), `--border`, font families, radius scales. Use these instead of hard-coding values.

**JS:** `static/js/main.js` is loaded globally (empty placeholder). Page-specific JS goes in `{% block scripts %}` in the relevant template — see the YouTube modal in `landing.html` for the pattern.

**Database:** Will be SQLite (`expense_tracker.db`, gitignored). Not yet wired up.
