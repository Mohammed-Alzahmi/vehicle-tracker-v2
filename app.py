from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime
import pytz

app = Flask(__name__)
DATA_FILE = "data.json"
UAE = pytz.timezone("Asia/Dubai")


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"regions": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.route("/")
def home():
    data = load_data()
    return render_template("home.html", regions=data["regions"])


@app.route("/add_region", methods=["POST"])
def add_region():
    data = load_data()
    name = request.form["region"]
    region_id = name.replace(" ", "_")

    data["regions"][region_id] = {
        "name": name,
        "records": []
    }
    save_data(data)
    return redirect(url_for("home"))


@app.route("/region/<region_id>")
def region_details(region_id):
    data = load_data()
    return render_template(
        "region_details.html",
        region=data["regions"][region_id],
        region_id=region_id
    )


@app.route("/register/<region_id>", methods=["GET", "POST"])
def register(region_id):
    data = load_data()

    if request.method == "POST":
        now = datetime.now(UAE).strftime("%H:%M")
        record = {
            "employee": request.form["employee"],
            "vehicle": request.form["vehicle"],
            "time": now
        }
        data["regions"][region_id]["records"].append(record)
        save_data(data)
        return render_template("index.html", success=True)

    return render_template("index.html", success=False)


@app.route("/qr/<region_id>")
def qr_view(region_id):
    return render_template("qr_view.html", region_id=region_id)
