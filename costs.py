from flask import request, redirect, render_template, session, flash, url_for
from trips_helpers import process_trip_id, owned, get_participants
from costs_helpers import add_costs, remove_costline
from app import db


def costs():

    if request.method == "POST":
        costhead = request.form.get("costhead")
        amount = request.form.get("amount")
        trip_id = request.form.get("trip_id")
        cost_party= request.form.get("cost_party")

        cost_trip = process_trip_id(trip_id)

        if owned(cost_trip):
            add_costs(trip_id, costhead, amount, cost_party)

        return redirect(url_for('cos', trip_id = trip_id))

    selected_trip_id = request.args.get("trip_id")
    selected_trip = process_trip_id(selected_trip_id)

    cost_lines = db.execute('''SELECT * 
                            FROM costs
                            LEFT JOIN users
                            ON cost_party = id
                            WHERE trip_id = ?
                            ''', selected_trip_id)
    
    total_cost = 0

    for cost_line in cost_lines:
        if not cost_line["username"]:
            cost_line["username"] = "Equal"
        total_cost += cost_line["cost_amount"]

    participants = get_participants(selected_trip_id)

    return render_template("costs.html", selected_trip = selected_trip, cost_lines = cost_lines, total_cost = total_cost, participants = participants)

def remove_cost():
    
    trip_id = request.form.get("trip_id")
    cost_id = request.form.get("cost_id")
    
    remove_costline(cost_id)

    return redirect(url_for('cos', trip_id = trip_id))
