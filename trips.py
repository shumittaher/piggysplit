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

def add_participents(trip_id, participent, guest):

    if not guest:
        db.execute("INSERT INTO participants (trip_id, participant_id) VALUES (?, ?)", trip_id, participent)

    else:
        db.execute("INSERT INTO participants (trip_id, guest_name) VALUES (?, ?)", trip_id, participent)
