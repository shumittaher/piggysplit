from flask import Flask, flash, redirect, render_template, request, jsonify, session
from costs_helpers import get_common_cost, get_induvidual_cost, total_trip_cost
from trips_helpers import get_participants, fetch_user_trips, process_trip_id
from payments_helpers import total_recevied, total_paid
from result_helpers import format_fixer, object_to_row, outstandings_row, format_fix_table



def result():

    trip_id = request.args.get("trip_id")
    trip_details = process_trip_id(trip_id)

    vendor_rows = []
    # vendor_outstanding = total_trip_cost(trip_id) - total_recevied(trip_id, 0)
    vendor_rows.append(object_to_row(outstandings_row("Vendor", (total_trip_cost(trip_id)),0,(total_recevied(trip_id, 0)), 0), True))
    
    # suggestions = [{"payer": "", "payee" : 0, "payable": -1 * vendor_outstanding}]

    outstandings = []
    participants = get_participants(trip_id)

    for participant in participants:

        payable_amounts = float(get_common_cost(trip_id) + get_induvidual_cost(trip_id, participant["id"]))
        paid_amount = total_paid(trip_id, participant["id"])
        recevied_amount = total_recevied(trip_id, participant["id"])
        participant_object = outstandings_row(participant["username"], 0, payable_amounts, recevied_amount, paid_amount)
        participant_row = object_to_row(participant_object)
        outstandings.append(participant_row)
    
        # suggestion = object_to_row(participant_object)
    
    suggestions = get_suggestions()
    
    return render_template("result.html", outstandings = format_fix_table(outstandings), vendor_rows = format_fix_table(vendor_rows), suggestions = suggestions, trip_details = trip_details)

def results_selection():
    
    participated_trips = fetch_user_trips(session["user_id"])
    return render_template("trip_selection.html", current_trips = participated_trips, route_name = "result")
 
def get_suggestions():
    return