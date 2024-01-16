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

        if (not username) or (password != password_2nd) or (not password or not password_2nd):
            flash("ERROR!")
            return redirect("/register")

        if db.execute("SELECT username FROM users WHERE username = ?", username):
            flash("Username Already Taken")
            return redirect("/register")

        passwordchecked = password_check(password)
        if passwordchecked["password_ok"] == False:
            flash(passwordchecked)
            return redirect("/register")

        hash_password = generate_password_hash(password)

        db.execute("INSERT INTO users (username, passwordhash) VALUES (?,?)", username, hash_password)

        return redirect("/login")
    
    else:
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        if not request.form.get("username"):
            flash("User Name Required")
            return redirect("/login")
        if not request.form.get("password"):
            flash("Password Required")
            return redirect("/login")
        
        users = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(users) != 1 or not check_password_hash(
            users[0]["passwordhash"], request.form.get("password")
        ):
            flash("Invalid User Name / Password")
            return redirect("/login")
        
        session["user_id"] = users[0]["id"]
        session["username"] = users[0]["username"]

        flash("Logged In")

        return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")