from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import re


from helpers import login_required

# Configure application
app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///piggysplit.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def hello_world():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_2nd = request.form.get("confirmation")

        # if not username:
        #     return apology("No username found", 400)

        # if db.execute("SELECT username FROM users WHERE username = ?", username):
        #     return apology("duplicate username found", 400)

        # if password != password_2nd:
        #     return apology("Invalid Password", 400)

        # if not password or not password_2nd:
        #     return apology("No password found", 400)

        passwordchecked = password_check(password)
        if passwordchecked["password_ok"] == False:
            flash("More Password Strength required")
            return render_template("register.html")

        hash_password = generate_password_hash(password)

        db.execute("INSERT INTO users (username, passwordhash) VALUES (?,?)", username, hash_password)

        return redirect("/login")
    else:
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():   
    return render_template("login.html")

def password_check(password):
    """
    Reference: https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-password-how-to-check-conditions

    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }
