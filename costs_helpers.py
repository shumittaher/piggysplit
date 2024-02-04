from app import db


def add_costs(trip_id, cost_head, cost_amount):
    db.execute("INSERT INTO costs (trip_id, cost_head, cost_amount) VALUES (?, ?, ?)", trip_id, cost_head, cost_amount)