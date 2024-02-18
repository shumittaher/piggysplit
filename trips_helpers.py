from flask import session, flash
from app import db


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

def remove_participants(relationship_id):
    db.execute("DELETE FROM participants WHERE relationship_id = ?", relationship_id)

def get_participants(selected_trip_id):
    return db.execute('''SELECT username, id
                              FROM participants 
                              JOIN users
                              ON participant_id = id
                              WHERE trip_id =?''', selected_trip_id)

def fetch_user_trips(user_id):
    return db.execute('''SELECT * 
               FROM trips
               LEFT JOIN participants
               ON trips.trip_id = participants.trip_id
               WHERE participant_id = ?''', user_id) 