from flask import request, redirect, render_template, session, flash
from app import db


def create():

    if request.method == "POST":
        tripname = request.form.get("tripname")
        tripdesc = request.form.get("tripdesc")
        db.execute("INSERT INTO trips (trip_title, trip_descrip, owner_id) VALUES (?,?,?)", tripname, tripdesc, session["user_id"])
        flash("Trip Recorded")
        return redirect("/create")

    return render_template("create.html")

def add_participents():

    db.execute("INSERT INTO trips (trip_title, trip_descrip, owner_id) VALUES (?,?,?)", tripname, tripdesc, session["user_id"])
