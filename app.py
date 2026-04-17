import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect(url_for("profile"))
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    def fail(msg):
        return render_template("register.html", error=msg, form_name=name, form_email=email)

    if not name:
        return fail("Name is required.")
    if not email or "@" not in email:
        return fail("A valid email is required.")
    if len(password) < 6:
        return fail("Password must be at least 6 characters.")
    if password != confirm_password:
        return fail("Passwords do not match.")

    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password)),
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return fail("An account with that email already exists.")

    return redirect(url_for("login") + "?registered=1")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect(url_for("profile"))
        registered = request.args.get("registered") == "1"
        return render_template("login.html", registered=registered)

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html", error="Invalid email or password")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()
    expense_count = conn.execute(
        "SELECT COUNT(*) FROM expenses WHERE user_id = ?", (session["user_id"],)
    ).fetchone()[0]
    conn.close()
    member_since = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %Y")

    transactions = [
        {"date": "Apr 15, 2026", "description": "Restaurant dinner",  "category": "Food",          "amount": 22.00},
        {"date": "Apr 13, 2026", "description": "Miscellaneous",      "category": "Other",         "amount": 15.00},
        {"date": "Apr 11, 2026", "description": "Clothing",           "category": "Shopping",      "amount": 60.00},
        {"date": "Apr 09, 2026", "description": "Movie tickets",      "category": "Entertainment", "amount": 20.00},
        {"date": "Apr 07, 2026", "description": "Pharmacy",           "category": "Health",        "amount": 45.00},
    ]

    categories = [
        {"name": "Bills",         "amount": 95.00, "count": 1},
        {"name": "Shopping",      "amount": 60.00, "count": 1},
        {"name": "Health",        "amount": 45.00, "count": 1},
        {"name": "Food",          "amount": 34.50, "count": 2},
        {"name": "Entertainment", "amount": 20.00, "count": 1},
        {"name": "Other",         "amount": 15.00, "count": 1},
        {"name": "Transport",     "amount":  8.00, "count": 1},
    ]

    total_spent = sum(c["amount"] for c in categories)
    top_category = categories[0]["name"]

    return render_template(
        "profile.html",
        user=user,
        expense_count=expense_count,
        member_since=member_since,
        transactions=transactions,
        categories=categories,
        total_spent=total_spent,
        top_category=top_category,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5002)
