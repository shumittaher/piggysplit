from app import db
from result_helpers import format_fix_table

def record_payment(payer_id, payee_id, trip_id, payment_desc, payment_amount):
    db.execute('''INSERT INTO payments
               (payer_id, paid_to, trip_id, payment_description, payment_amount)
               VALUES (?, ?, ?, ?, ?) ''', 
               payer_id, payee_id, trip_id, payment_desc, payment_amount)
    
def fetch_tripwise_payments(trip_id):
    return format_fix_table(db.execute('''SELECT *
                      FROM payments
                      LEFT JOIN users
                      ON paid_to = id
                      WHERE trip_id = ?
                      ''', trip_id), "payment_amount")

def delete_payment(payment_id):
    db.execute('''DELETE FROM payments
               WHERE payment_id = ?''', payment_id)

def fetch_tripwise_payments_as_for_id(trip_id, id, placement):
    return db.execute(f"SELECT * FROM payments LEFT JOIN users ON {placement} = id WHERE trip_id = ? AND {placement} = ?", trip_id, id)

def total_recevied(trip_id, payee_id):

    payments = fetch_tripwise_payments_as_for_id(trip_id, payee_id, "paid_to")
    return sum_payment(payments)

def total_paid(trip_id, payer_id):
    
    payments = fetch_tripwise_payments_as_for_id(trip_id, payer_id, "payer_id")
    return sum_payment(payments)

def sum_payment(payments):
    amount = 0
    for row in payments:
        amount += row["payment_amount"]
    return amount