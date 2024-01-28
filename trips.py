from flask import request, redirect, render_template, session, flash, url_for
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
    
    if request.method == "POST":

        participants = request.form.getlist("participants[]")
        trip_id = request.form.get("trip_id")
        if not owned(trip_id):
            flash("Invalid")
            return redirect("/")
        
        for participant in participants:
            if not check_existing(trip_id, participant):
                add_participents(trip_id, participant)
            else:
                flash("Existing Person Not Added")

        return redirect(url_for('sel', trip_id = trip_id))
        
    selected_trip_id = request.args.get("trip_id")
    selected_trip = db.execute("SELECT * FROM trips WHERE trip_id = ?", selected_trip_id)

    if not owned(selected_trip_id):
        flash("Invalid")
        return redirect("/")

    friends = db.execute("SELECT id,username FROM users")

    return render_template("tripselected.html", selected_trip = selected_trip, friends = friends )

def add_participents(trip_id, participent, guest = ""):
    if not guest:
        db.execute("INSERT INTO participants (trip_id, participant_id) VALUES (?, ?)", trip_id, participent)
    else:
        db.execute("INSERT INTO participants (trip_id, guest_name) VALUES (?, ?)", trip_id, participent)


def owned(trip_id):
    selected_trip = db.execute("SELECT * FROM trips WHERE trip_id = ?", trip_id)
    return (selected_trip[0]["owner_id"]) == session["user_id"]

def check_existing(trip_id, user_id):
    trips = db.execute("SELECT * FROM participants WHERE trip_id=?", trip_id)
    for trip in trips:
        if (int(trip["participant_id"])) == int(user_id):
            return True
    return False