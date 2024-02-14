from app import db

def record_payment(payer_id, payee_id, trip_id, payment_desc, payment_amount):
    db.execute('''INSERT INTO payments
               (payer_id, paid_to, trip_id, payment_description, payment_amount)
               VALUES (?, ?, ?, ?, ?) ''', 
               payer_id, payee_id, trip_id, payment_desc, payment_amount)