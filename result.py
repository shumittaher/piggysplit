from flask import Flask, flash, redirect, render_template, request, jsonify
from costs_helpers import get_common_cost, get_induvidual_cost, total_trip_cost
from trips_helpers import get_participants


def result():

    trip_id = request.args.get("trip_id")

    outstandings = [{"recipient":"vendor", "amount": -1 * total_trip_cost(trip_id)}]
    
    participants = get_participants(trip_id)

    for participant in participants:
        participant_outstanding = {"recipient":participant["username"], "amount": get_common_cost(trip_id) + get_induvidual_cost(trip_id, participant["id"])}
        outstandings.append(participant_outstanding)

    return render_template("result.html", outstandings = outstandings)