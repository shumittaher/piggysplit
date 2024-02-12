from flask import render_template, session, request
from trips_helpers import fetch_user_trips

def payments():

    if request.method == "POST":
        participant_id = request.form.get("participant_id")
        payment_amount = request.form.get("payment_amount")
        trip_id = request.form.get("trip_id")

    user_id = session.get("user_id")
    users_trips = fetch_user_trips(user_id)

    return render_template("payments.html", users_trips = users_trips)