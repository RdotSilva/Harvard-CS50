import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # Form validation used if incase JavaScript is disabled.
    if not request.form.get("name") or not request.form.get("gender"):
        return render_template("error.html", message="One or more fields missing.")

    # Write form data to csv file.
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("name"), request.form.get("gender"), request.form.get("age")))
    file.close()

    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    # Display data from vsc file.
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    people = list(reader)
    file.close()

    return render_template("sheet.html", people=people)

