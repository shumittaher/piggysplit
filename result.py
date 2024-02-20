from flask import Flask, flash, redirect, render_template, request, jsonify, session
from costs_helpers import get_common_cost, get_induvidual_cost, total_trip_cost
from trips_helpers import get_participants, fetch_user_trips, process_trip_id
from payments_helpers import total_recevied, total_paid
from result_helpers import format_fixer



def result():

    trip_id = request.args.get("trip_id")
    trip_details = process_trip_id(trip_id)

    vendor_row = {"party" : "Vendor", 
                  "receivable_amount": format_fixer(total_trip_cost(trip_id)), 
                  "received_amount": format_fixer(total_recevied(trip_id, 0)), 
                  "outstanding_amount":format_fixer(total_trip_cost(trip_id) - total_recevied(trip_id, 0))}


    outstandings = []
    participants = get_participants(trip_id)

    for participant in participants:

        payable_amounts = float(get_common_cost(trip_id) + get_induvidual_cost(trip_id, participant["id"]))
        paid_amount = total_paid(trip_id, participant["id"])
        recevied_amount = total_recevied(trip_id, participant["id"])
        participant_object = outstandings_row(participant["username"], payable_amounts, recevied_amount, paid_amount)
        participant_row = object_to_row(participant_object)
        outstandings.append(participant_row)

    return render_template("result.html", outstandings = outstandings, vendor_row = vendor_row, trip_details = trip_details)

class outstandings_row:
    def __init__(self, party, payable_amounts, received_amount, paid_amounts):
        self.party= party
        self.received_amount = received_amount
        self.payable_amounts = payable_amounts
        self.paid_amounts = paid_amounts

    def calculate_outstanding(self):
        return (self.payable_amounts - self.paid_amounts + self.received_amount)
    

def object_to_row(obj):
    return {
                "party" : obj.party, 
                "received_amount": format_fixer(obj.received_amount), 
                "payable_amounts":format_fixer(obj.payable_amounts), 
                "paid_amounts": format_fixer(obj.paid_amounts), 
                "outstanding_amount":format_fixer(obj.calculate_outstanding())
            }

def results_selection():
    
    participated_trips = fetch_user_trips(session["user_id"])
    return render_template("trip_selection.html", current_trips = participated_trips, route_name = "result")
 
