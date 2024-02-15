from flask import render_template, session, request, redirect
from trips_helpers import fetch_user_trips
from payments_helpers import record_payment, fetch_tripwise_payments, delete_payment

def payments():
    
    user_id = session.get("user_id")
    users_trips = fetch_user_trips(user_id)

    return render_template("payments.html", users_trips = users_trips)