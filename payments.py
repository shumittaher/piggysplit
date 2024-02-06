from flask import render_template, session
from trips_helpers import fetch_user_trips

def payments():

    user_id = session.get("user_id")
    users_trips = fetch_user_trips(user_id)

    return render_template("payments.html", users_trips = users_trips)