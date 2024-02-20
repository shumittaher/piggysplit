from flask import request, redirect, render_template, session, flash, url_for
from app import db
from trips_helpers import process_trip_id, owned, check_existing, add_participents, remove_participant, get_participants, fetch_owned_trips

def trips():
    
    owned_trips = fetch_owned_trips(session["user_id"])
    return render_template("trips.html", current_trips = owned_trips, route_name = "select")

def create():
    tripname = request.form.get("tripname")
    tripdesc = request.form.get("tripdesc")
    db.execute("INSERT INTO trips (trip_title, trip_descrip, owner_id) VALUES (?,?,?)", tripname, tripdesc, session["user_id"])
    flash("Trip Recorded")
    return redirect("/trips")

def select_participants():
  
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

def remove_participants():

    relationship_id = request.form.get("relationship_id")
    remove_participant(relationship_id)
    trip_id = request.form.get("trip_id")

    return redirect(url_for('sel', trip_id = trip_id))

def participant_selection():
    
    owned_trips = fetch_owned_trips(session["user_id"])
    return render_template("trip_selection.html", current_trips = owned_trips, route_name = "select")
 