from flask import Flask, flash, redirect, render_template, request, jsonify
from costs_helpers import get_common_cost, get_induvidual_cost, total_trip_cost
from trips_helpers import get_participants


def result():

    trip_id = request.args.get("trip_id")

    outstandings = [{"recipient":"Vendor", "amount": total_trip_cost(trip_id), "receivable" : 1}]
    
    participants = get_participants(trip_id)

    for participant in participants:
        amount = float(get_common_cost(trip_id) + get_induvidual_cost(trip_id, participant["id"]))
        participant_outstanding = {"recipient":participant["username"], "amount": amount, "receivable" : 0}
        outstandings.append(participant_outstanding)

    return render_template("result.html", outstandings = outstandings)