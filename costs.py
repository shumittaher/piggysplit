from flask import request, redirect, render_template, session, flash, url_for
from trips_helpers import process_trip_id, owned, get_participants, fetch_owned_trips
from costs_helpers import add_costs, remove_costline, total_trip_cost, fetch_costlines
from app import db
from result_helpers import format_fixer, format_fix_table

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

    cost_lines = format_fix_table(fetch_costlines(selected_trip_id))
  
    total_cost = format_fixer(total_trip_cost(selected_trip_id))

    participants = get_participants(selected_trip_id)

    return render_template("costs.html", selected_trip = selected_trip, cost_lines = cost_lines, total_cost = total_cost, participants = participants)

def remove_cost():
    
    trip_id = request.form.get("trip_id")
    cost_id = request.form.get("cost_id")
    
    remove_costline(cost_id)

    return redirect(url_for('cos', trip_id = trip_id))


def cost_selection():
    
    owned_trips = fetch_owned_trips(session["user_id"])
    return render_template("trip_selection.html", current_trips = owned_trips, route_name = "costs")
