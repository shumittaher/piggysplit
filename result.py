from flask import Flask, flash, redirect, render_template, request, jsonify
from costs_helpers import get_common_cost, get_induvidual_cost, total_trip_cost
from trips_helpers import get_participants
from payments_helpers import total_recevied, total_paid


def result():

    trip_id = request.args.get("trip_id")

    outstandings = []

    vendor_row = outstandings_row("Vendor", total_trip_cost(trip_id), total_recevied(trip_id, 0), 0, 0)
    outstandings.append(vendor_row)

    participants = get_participants(trip_id)

    for participant in participants:

        payable_amounts = float(get_common_cost(trip_id) + get_induvidual_cost(trip_id, participant["id"]))

        # participant_outstanding = {"recipient":participant["username"], "amount": outstanding_amounts, "receivable" : 0}
        # outstandings.append(participant_outstanding)

    return render_template("result.html", outstandings = outstandings)

class outstandings_row:
    def __init__(self, party, receivable_amount, received_amount, payable_amounts, paid_amounts):
        self.party= party
        self.receivable_amount = receivable_amount
        self.received_amount = received_amount
        self.payable_amounts = payable_amounts
        self.paid_amounts = paid_amounts
