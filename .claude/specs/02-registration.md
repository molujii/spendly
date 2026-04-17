# Spec: Registration

## Overview
This step wires up the registration form so new users can create an account. The `/register` route gains a POST handler that validates the submitted name, email, and password, checks for duplicate emails, hashes the password with werkzeug, inserts the new user into the `users` table, and redirects to the login page on success. This is the first user-facing write operation in Spendly and establishes the session-less auth foundation that Step 3 (Login) will build on.

## Depends on
- Step 01 — Database Setup (users table must exist, `get_db()` must be available)

## Routes
- `GET /register` — render the registration form — public (already exists, no change needed)
- `POST /register` — handle form submission, validate, insert user, redirect — public

## Database changes
No database changes. The `users` table created in Step 01 is sufficient.

## Templates
- **Modify:** `templates/register.html`
  - Add `method="POST"` and `action="/register"` to the `<form>` tag
  - Add `name` attributes to all inputs: `name`, `email`, `password`, `confirm_password`
  - Add a `{{ error }}` flash/inline error display block below the form heading
  - Ensure CSRF is not required (not in scope for this step)

## Files to change
- `app.py` — convert `GET`-only `/register` route to handle both GET and POST; add import for `request`, `redirect`, `url_for`, `flash`, `session`
- `templates/register.html` — add form attributes and error display (see Templates above)

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate server-side: name non-empty, valid email format (basic check), password ≥ 6 chars, passwords match
- If email already exists (UNIQUE constraint violation), show a user-friendly inline error — do not let the exception propagate
- On success, redirect to `/login` with a success message (use `flash` or a query param `?registered=1`)
- Do not log the user in automatically after registration — that is Step 3

## Definition of done
- [ ] Visiting `/register` renders the form (GET still works)
- [ ] Submitting with all valid fields creates a new row in `users` with a hashed password
- [ ] After successful registration, user is redirected to `/login`
- [ ] Submitting with mismatched passwords shows an inline error and does not insert a row
- [ ] Submitting with an already-registered email shows an inline error and does not insert a duplicate row
- [ ] Submitting with an empty name or empty email shows an inline error
- [ ] Password is stored as a hash (not plaintext) — verifiable by inspecting `spendly.db` directly
- [ ] All validation errors re-render the form (no data lost in the name/email fields)
