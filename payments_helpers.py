from app import db

def record_payment(payer_id, payee_id, trip_id):
    db.execute('''INSERT INTO payments
               (,,trip_id)
               VALUES (?, ?, ?) ''', payer_id, payee_id, trip_id)