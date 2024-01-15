from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash



from helpers import login_required, password_check

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