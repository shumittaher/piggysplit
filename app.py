from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required

db = SQL("sqlite:///piggysplit.db")
from credentials import register, login, logout
from trips import trips, create, select

# Configure application
app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
def reg():
    return register()
    
@app.route("/login", methods=["GET", "POST"])
def logi():
    return login()

@app.route("/logout")
def logo():
    return logout()

@app.route("/trips")
@login_required
def trip():
    return trips()

@app.route("/create", methods=["POST"])
@login_required
def crea():
    return create()

@app.route("/select", methods=["GET","POST"])
@login_required
def sel():
    return select()