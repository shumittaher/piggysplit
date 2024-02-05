from app import db
from trips_helpers import get_participants



def add_costs(trip_id, cost_head, cost_amount, cost_party):
    db.execute("INSERT INTO costs (trip_id, cost_head, cost_amount, cost_party) VALUES (?, ?, ?, ?)", trip_id, cost_head, cost_amount, cost_party)

def remove_costline(cost_id):
    db.execute("DELETE FROM costs WHERE cost_id = ?", cost_id)

def total_trip_cost(trip_id):

    cost_lines = fetch_costlines(trip_id)
    
    total_cost = 0

    for cost_line in cost_lines:
        if not cost_line["username"]:
            cost_line["username"] = "Equal"
        total_cost += cost_line["cost_amount"]

    return total_cost

def fetch_costlines(trip_id):
    return db.execute('''SELECT * 
                            FROM costs
                            LEFT JOIN users
                            ON cost_party = id
                            WHERE trip_id = ?
                            ''', trip_id)

def get_common_cost(trip_id):
    cost_lines = fetch_costlines(trip_id)
    participants = get_participants(trip_id)
    participant_count = len(participants)

    total_common_cost = 0
    
    for cost_line in cost_lines:
        if cost_line["cost_party"] ==0:
            total_common_cost += cost_line["cost_amount"]

    return total_common_cost / participant_count

def get_induvidual_cost(trip_id, person_id):

    individual_cost_total = 0

    cost_lines = fetch_costlines(trip_id)
    for cost_line in cost_lines:
        if cost_line["cost_party"] == person_id:
            individual_cost_total += cost_line["cost_amount"]

    return individual_cost_total