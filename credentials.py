from cs50 import SQL
from flask import flash, redirect, render_template, request, session
from helpers import password_check
from werkzeug.security import check_password_hash, generate_password_hash

db = SQL("sqlite:///piggysplit.db")

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

def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")