from flask import request, redirect, render_template, session
from app import db


def create():

    if request.method == "POST":
        tripname = request.form.get("tripname")
        tripdesc = request.form.get("tripdesc")
        db.execute("INSERT INTO trips (trip_title, trip_descrip, owner_id) VALUES (?,?,?)", tripname, tripdesc, session["user_id"])
        return redirect("/create")

    return render_template("create.html")