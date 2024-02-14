from flask import render_template, session, request
from trips_helpers import fetch_user_trips
from payments_helpers import record_payment

def payments():
    
    user_id = session.get("user_id")

    if request.method == "POST":
        participant_id = request.form.get("participant_id")
        payment_amount = request.form.get("payment_amount")
        payment_desc = request.form.get("payment_desc")
        trip_id = request.form.get("trip_id")
        record_payment(user_id, participant_id, trip_id, payment_desc, payment_amount)

    users_trips = fetch_user_trips(user_id)

    return render_template("payments.html", users_trips = users_trips)