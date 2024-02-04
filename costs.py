from flask import request, redirect, render_template, session, flash, url_for
from trips_helpers import process_trip_id, owned
from costs_helpers import add_costs

def costs():

    if request.method == "POST":
        costhead = request.form.get("costhead")
        amount = request.form.get("amount")
        trip_id = request.form.get("trip_id")

        cost_trip = process_trip_id(trip_id)

        if owned(cost_trip):
            add_costs(trip_id, costhead, amount)

        return redirect(url_for('cos', trip_id = trip_id))

    selected_trip_id = request.args.get("trip_id")
    selected_trip = process_trip_id(selected_trip_id)



    return render_template("costs.html", selected_trip = selected_trip)