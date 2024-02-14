from cs50 import SQL
from flask import Flask, render_template, request, jsonify
from flask_session import Session
db = SQL("sqlite:///piggysplit.db")

from credentials import register, login, logout,login_required, session
from trips import trips, create, select, remove, process_trip_id, get_participants
from costs import costs, remove_cost
from payments import payments, fetch_tripwise_payments, record_payment
from result import result

# Configure application
app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def reg():
    return register()
    
@app.route("/login", methods=["GET", "POST"])
def logi():
    return login()

@app.route("/logout")
def logo():
    return logout()

@app.route("/trips")
@login_required
def trip():
    return trips()

@app.route("/create", methods=["POST"])
@login_required
def crea():
    return create()

@app.route("/select", methods=["GET","POST"])
@login_required
def sel():
    return select()

@app.route("/remove", methods=["POST"])
@login_required
def rem():
    return remove()

@app.route("/costs", methods=["GET","POST"])
@login_required
def cos():
    return costs()

@app.route("/payments")
@login_required
def pay():
    return payments()

@app.route("/remove_cost", methods=["POST"])
@login_required
def rem_cost():
    return remove_cost()

@app.route("/result", methods=["GET","POST"])
@login_required
def res():
    return result()

@app.route("/trip_payments", methods=["POST"])
def process_data():
    trip_id = request.get_json().get('trip_id')
    trip_data = process_trip_id(trip_id)
    participants_data = get_participants(trip_id)
    payments_data = fetch_tripwise_payments(trip_id)

    return jsonify({'trip_data': trip_data, 'participants_data': participants_data, 'payments_data': payments_data})

@app.route("/record_payments", methods=["POST"])
def record_payments():
    payments_row = request.get_json().get('payments_row')

    participant_id = payments_row["participant_id"]
    payment_amount = payments_row["payment_amount"]
    payment_desc = payments_row["payment_desc"]
    trip_id = payments_row["trip_id"]

    user_id = session.get("user_id")

    record_payment(user_id, participant_id, trip_id, payment_desc, payment_amount)

    payments_data = fetch_tripwise_payments(trip_id)

    return jsonify({'payments_data': payments_data})

