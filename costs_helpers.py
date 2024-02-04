from app import db


def add_costs(trip_id, cost_head, cost_amount, cost_party):
    db.execute("INSERT INTO costs (trip_id, cost_head, cost_amount, cost_party) VALUES (?, ?, ?, ?)", trip_id, cost_head, cost_amount, cost_party)

def remove_costline(cost_id):
    db.execute("DELETE FROM costs WHERE cost_id = ?", cost_id)