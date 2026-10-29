"""
Password Strength Checker
A beginner-friendly Flask app that rates a password as Weak, Medium or Strong.

Privacy note:
  * The password is only used inside the analyze_password() function.
  * It is never saved to a file or database, never printed, and never logged.
  * The form uses POST (not GET), so the password never appears in the URL.
  * The password box is always left empty when the page reloads.
"""

import logging
import re

from flask import Flask, render_template, request

app = Flask(__name__)

# Hide the web server's request log so nothing about requests ends up in the terminal.
logging.getLogger("werkzeug").setLevel(logging.ERROR)

# A tiny list of very common passwords. Real checkers use lists with millions.
COMMON_PASSWORDS = {
    "password", "password1", "password123", "123456", "12345678", "123456789",
    "1234567890", "qwerty", "qwerty123", "abc123", "letmein", "welcome",
    "admin", "iloveyou", "monkey", "dragon", "football", "baseball",
    "login", "master", "sunshine", "princess", "passw0rd", "p@ssw0rd",
    "111111", "000000", "123123", "trustno1",
}

MAX_LENGTH = 128  # ignore absurdly long input


def analyze_password(password: str) -> dict:
    """Check a password and return a result dictionary. Nothing is stored."""
    password = password[:MAX_LENGTH]

    # --- The five main checks -------------------------------------------
    has_length_8 = len(password) >= 8
    has_length_12 = len(password) >= 12
    has_upper = re.search(r"[A-Z]", password) is not None
    has_lower = re.search(r"[a-z]", password) is not None
    has_digit = re.search(r"\d", password) is not None
    has_special = re.search(r"[^A-Za-z0-9\s]", password) is not None

    # --- Extra weakness checks ------------------------------------------
    is_common = password.lower() in COMMON_PASSWORDS
    has_repeats = re.search(r"(.)\1\1", password) is not None  # e.g. "aaa"

    checks = [
        {"label": "At least 8 characters", "passed": has_length_8},
        {"label": "At least 12 characters (recommended)", "passed": has_length_12},
        {"label": "Contains an uppercase letter (A-Z)", "passed": has_upper},
        {"label": "Contains a lowercase letter (a-z)", "passed": has_lower},
        {"label": "Contains a number (0-9)", "passed": has_digit},
        {"label": "Contains a special character (! @ # $ ...)", "passed": has_special},
    ]

    # Score = how many checks passed (0 to 6)
    score = sum(1 for c in checks if c["passed"])

    # --- Decide the rating ----------------------------------------------
    if is_common or not has_length_8 or score <= 3:
        label = "Weak"
    elif score == 6 and not has_repeats:
        label = "Strong"
    else:
        label = "Medium"

    # --- Build suggestions ----------------------------------------------
    suggestions = []
    if is_common:
        suggestions.append("This is a very common password. Attackers try these first, so choose something unique.")
    if not has_length_8:
        suggestions.append("Make it at least 8 characters long.")
    elif not has_length_12:
        suggestions.append("Aim for 12 or more characters. Longer passwords are much harder to crack.")
    if not has_upper:
        suggestions.append("Add an uppercase letter (A-Z).")
    if not has_lower:
        suggestions.append("Add a lowercase letter (a-z).")
    if not has_digit:
        suggestions.append("Add a number (0-9).")
    if not has_special:
        suggestions.append("Add a special character such as ! @ # $ % or &.")
    if has_repeats:
        suggestions.append("Avoid repeating the same character three or more times in a row (like 'aaa').")
    if label == "Strong":
        suggestions.append("Great! Use a different strong password for every account, and consider a password manager.")

    return {
        "label": label,
        "css_class": label.lower(),
        "score": score,
        "max_score": len(checks),
        "checks": checks,
        "suggestions": suggestions,
    }


@app.after_request
def add_privacy_headers(response):
    """Ask the browser not to cache pages, so results are not kept around."""
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if password:
            result = analyze_password(password)
        # 'password' goes out of scope here. We never save or print it.
    return render_template("index.html", result=result)


if __name__ == "__main__":
    # debug=False keeps things quieter and safer.
    app.run(host="127.0.0.1", port=5000, debug=False)
