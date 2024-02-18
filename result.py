from flask import Flask, flash, redirect, render_template, request, jsonify
from costs_helpers import get_common_cost, get_induvidual_cost, total_trip_cost
from trips_helpers import get_participants
from payments_helpers import total_recevied, total_paid


def result():

    trip_id = request.args.get("trip_id")

    outstandings = []

    vendor_object = outstandings_row("Vendor", total_trip_cost(trip_id),  0, total_recevied(trip_id, 0), 0)
    vendor_row = object_to_row(vendor_object)
    outstandings.append(vendor_row)

    participants = get_participants(trip_id)

    for participant in participants:

        payable_amounts = float(get_common_cost(trip_id) + get_induvidual_cost(trip_id, participant["id"]))
        paid_amount = total_paid(trip_id, participant["id"])
        recevied_amount = total_recevied(trip_id, participant["id"])
        participant_object = outstandings_row(participant["username"], 0,  payable_amounts, recevied_amount, paid_amount)
        participant_row = object_to_row(participant_object)
        outstandings.append(participant_row)

    return render_template("result.html", outstandings = outstandings)

class outstandings_row:
    def __init__(self, party, receivable_amount, payable_amounts, received_amount, paid_amounts):
        self.party= party
        self.receivable_amount = receivable_amount
        self.received_amount = received_amount
        self.payable_amounts = payable_amounts
        self.paid_amounts = paid_amounts

    def calculate_outstanding(self):
        return (self.payable_amounts - self.paid_amounts - self.receivable_amount + self.received_amount)
    

def object_to_row(obj):
    return {"party" : obj.party, 
            "receivable_amount": obj.receivable_amount, 
            "received_amount": obj.received_amount, 
            "payable_amounts":obj.payable_amounts, 
            "paid_amounts": obj.paid_amounts, 
            "outstanding_amount":obj.calculate_outstanding()}
