from app import db

def record_payment(payer_id, payee_id, trip_id, payment_desc, payment_amount):
    db.execute('''INSERT INTO payments
               (payer_id, paid_to, trip_id, payment_description, payment_amount)
               VALUES (?, ?, ?, ?, ?) ''', 
               payer_id, payee_id, trip_id, payment_desc, payment_amount)
    
def fetch_tripwise_payments(trip_id):
    return db.execute('''SELECT *
                      FROM payments
                      LEFT JOIN users
                      ON paid_to = id
                      WHERE trip_id = ?
                      ''', trip_id)

def delete_payment(payment_id):
    db.execute('''DELETE FROM payments
               WHERE payment_id = ?''', payment_id)