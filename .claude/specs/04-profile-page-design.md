# Spec: Profile Page Design

## Overview
This step replaces the `/profile` placeholder with a real, styled profile page. Logged-in users can view their account details (name, email, member-since date) and see a summary of their activity (total expenses recorded). The page is read-only in this step — editing profile fields is out of scope. It also wires the navbar's user name/icon up to link to `/profile`, giving the app its first authenticated interior page.

## Depends on
- Step 01 — Database Setup (`users` table must exist, `get_db()` must be available)
- Step 02 — Registration (user records exist in the DB)
- Step 03 — Login and Logout (`session['user_id']` and `session['user_name']` must be set)

## Routes
- `GET /profile` — render the profile page for the currently logged-in user — logged-in only (redirect to `/login` if not authenticated)

## Database changes
No database changes. The existing `users` and `expenses` tables are sufficient.

## Templates
- **Create:** `templates/profile.html`
  - Extends `base.html`
  - Displays a profile card with: user's name, email, and `created_at` date formatted as "Member since Month YYYY"
  - Displays a stats row: total number of expenses recorded for this user
  - Has a visible "Logout" action link/button styled with `--accent` variables
- **Modify:** `templates/base.html`
  - When `session.user_id` is set, add a "Profile" link in the nav alongside the existing "Logout" link

## Files to change
- `app.py`
  - Replace the `/profile` placeholder with a real route handler
  - Query the `users` table for the logged-in user's record using `session['user_id']`
  - Query the `expenses` table to count this user's total expenses
  - Pass `user` and `expense_count` to the template
  - Redirect to `url_for('login')` if `session.get('user_id')` is falsy
- `templates/base.html`
  - Add `<a href="{{ url_for('profile') }}">Profile</a>` inside the logged-in nav block

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with werkzeug (no password changes in this step, but maintain the principle)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Redirect unauthenticated visitors to `/login` (do not show a 403)
- Do not implement profile editing — this step is display-only
- Format `created_at` in the template using Jinja's `strptime`/`strftime` or Python's `datetime` in the route — do not display raw ISO strings to the user
- Expense count query must be scoped to `WHERE user_id = ?` — never expose other users' data

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Visiting `/profile` while logged in renders the profile page (no 500, no placeholder string)
- [ ] The page displays the correct name and email for the logged-in user
- [ ] The "Member since" date is human-readable (e.g. "April 2026"), not a raw ISO string
- [ ] The page shows the correct total expense count for the logged-in user
- [ ] The navbar shows a "Profile" link when logged in, which navigates to `/profile`
- [ ] The profile page has a working "Logout" link that clears the session
- [ ] The page is styled consistently with the rest of the app (uses `--accent`, `--ink`, `--paper` CSS variables)
- [ ] No other user's data is ever accessible via this route
