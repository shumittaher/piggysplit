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
        trip = process_trip_id(trip_id)

        # validations
        if not "owner_id" in trip:
            return redirect("/")

        if not owned(trip):
            flash("Invalid")
            return redirect("/")
        #end of validataions
        
        for participant in participants:
            if not check_existing(trip_id, participant):
                add_participents(trip_id, participant)
            else:
                flash("Existing Person Not Added")

        return redirect(url_for('sel', trip_id = trip_id))

    selected_trip_id = request.args.get("trip_id")
    selected_trip = process_trip_id(selected_trip_id)

    # validations
    if not "owner_id" in selected_trip:
        return redirect("/")

    if not owned(selected_trip):
        flash("Unauthorized")
        return redirect("/")
    #end of validataions

    friends = db.execute("SELECT id,username FROM users")

    return render_template("tripselected.html", selected_trip = selected_trip, friends = friends )

def add_participents(trip_id, participent, guest = ""):
    if not guest:
        db.execute("INSERT INTO participants (trip_id, participant_id) VALUES (?, ?)", trip_id, participent)
    else:
        db.execute("INSERT INTO participants (trip_id, guest_name) VALUES (?, ?)", trip_id, participent)

def owned(selected_trip):
    return (selected_trip["owner_id"]) == session["user_id"]

def check_existing(trip_id, user_id):
    trips = db.execute("SELECT * FROM participants WHERE trip_id=?", trip_id)
    for trip in trips:
        if (int(trip["participant_id"])) == int(user_id):
            return True
    return False

def process_trip_id(id):
    selected_trip = {}
    selected_trip_array = db.execute("SELECT * FROM trips WHERE trip_id = ?", id)
    if selected_trip_array:
        selected_trip = selected_trip_array[0]
    else:
        flash("Invalid")
    return selected_trip