# Spec: Login and Logout

## Overview
This step wires up the login and logout flows so registered users can authenticate and end their session. The `/login` route gains a POST handler that looks up the user by email, verifies the password with werkzeug, and stores the user's `id` and `name` in a Flask session on success. The `/logout` route clears that session and redirects to the landing page. This step also adds a `secret_key` to the Flask app (required for signed sessions) and updates the navbar to show the correct links depending on whether the user is logged in.

## Depends on
- Step 01 — Database Setup (`users` table must exist, `get_db()` must be available)
- Step 02 — Registration (users must already exist in the DB to log in)

## Routes
- `GET /login` — render the login form — public (already exists, gains `?registered=1` banner)
- `POST /login` — validate credentials, set session, redirect to dashboard or expenses — public
- `GET /logout` — clear session, redirect to `/` — public (safe to call when not logged in)

## Database changes
No database changes. The `users` table from Step 01 is sufficient.

## Templates
- **Modify:** `templates/login.html`
  - Add `method="POST"` and `action="/login"` to the `<form>` tag
  - Add `name` attributes to inputs: `email`, `password`
  - Add an inline error display block (`{{ error }}`)
  - Add a success banner shown when `?registered=1` is in the query string
- **Modify:** `templates/base.html`
  - Update navbar links: when `session.user_id` is set, show "Logout" (and optionally the user's name); otherwise show "Login" and "Register"

## Files to change
- `app.py`
  - Add `app.secret_key` (use a hard-coded dev string for now; note it must be changed for production)
  - Add `session`, `check_password_hash` imports
  - Convert `GET`-only `/login` route to handle both GET and POST
  - Implement POST handler: look up user by email, verify hash, set `session['user_id']` and `session['user_name']`, redirect
  - Replace `/logout` placeholder with real handler: `session.clear()`, redirect to `url_for('landing')`
- `templates/login.html` — add form attributes, error display, and registered success banner (see Templates)
- `templates/base.html` — conditional navbar links based on session state (see Templates)

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available via Flask's dependency on werkzeug.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On failed login, show a single vague error ("Invalid email or password") — do not reveal which field was wrong
- On successful login, redirect to `/expenses` (placeholder is fine for now) or `/` if that route doesn't exist yet
- `secret_key` must be set before any session operations; use a fixed dev string like `"dev-secret-change-me"` — do not generate it randomly at startup (sessions would break on restart)
- Do not implement "remember me" or session expiry — out of scope
- Logout must work even if the user is not logged in (no error should be raised)

## Definition of done
- [ ] Visiting `/login` renders the login form (GET still works)
- [ ] Submitting valid credentials sets a session and redirects away from `/login`
- [ ] After login, the navbar shows "Logout" instead of "Login" / "Register"
- [ ] Submitting an unknown email shows "Invalid email or password" inline error
- [ ] Submitting the correct email with the wrong password shows the same vague error
- [ ] Visiting `/logout` clears the session and redirects to the landing page
- [ ] After logout, the navbar shows "Login" and "Register" again
- [ ] Visiting `/logout` when not logged in redirects cleanly (no 500 error)
- [ ] The `?registered=1` success banner is visible on `/login` after a successful registration
