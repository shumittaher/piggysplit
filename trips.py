from flask import request, redirect, render_template, session, flash, url_for
from app import db
from trips_helpers import process_trip_id, owned, check_existing, add_participents, remove_participants, get_participants

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
    participants = get_participants(selected_trip_id)

    return render_template("tripselected.html", selected_trip = selected_trip, friends = friends, participants = participants)

def remove():

    relationship_id = request.form.get("relationship_id")
    remove_participants(relationship_id)
    trip_id = request.form.get("trip_id")

    return redirect(url_for('sel', trip_id = trip_id))
 