from flask import request, redirect, render_template, session, flash
from app import db

def trips():
    
    current_trips = db.execute("SELECT * FROM trips WHERE owner_id = ? AND closed = FALSE", session["user_id"])
    return render_template("trips.html", current_trips = current_trips)

def create():
    tripname = request.form.get("tripname")
    tripdesc = request.form.get("tripdesc")
    db.execute("INSERT INTO trips (trip_title, trip_descrip, owner_id) VALUES (?,?,?)", tripname, tripdesc, session["user_id"])
    flash("Trip Recorded")
    return redirect("/trips")

def select():

    selected_trip_id = request.form.get("trip_id")
    print(selected_trip_id)
    return render_template("tripselected.html", selected_trip_id = selected_trip_id)

def add_participents(trip_id, participent, guest):
    if not guest:
        db.execute("INSERT INTO participants (trip_id, participant_id) VALUES (?, ?)", trip_id, participent)
    else:
        db.execute("INSERT INTO participants (trip_id, guest_name) VALUES (?, ?)", trip_id, participent)
