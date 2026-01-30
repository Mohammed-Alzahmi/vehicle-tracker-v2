from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"regions": {}, "records": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    data = load_data()
    return render_template("home.html", regions=data["regions"])

@app.route("/add_region", methods=["POST"])
def add_region():
    name = request.form["region_name"]
    data = load_data()
    region_id = name.replace(" ", "_")
    data["regions"][region_id] = name
    save_data(data)
    return redirect(url_for("home"))

@app.route("/region/<region_id>")
def region_details(region_id):
    data = load_data()
    records = [r for r in data["records"] if r["region"] == region_id]
    return render_template(
        "region_details.html",
        region_name=data["regions"][region_id],
        region_id=region_id,
        records=records
    )

@app.route("/qr/<region_id>")
def qr_view(region_id):
    return render_template("qr_view.html", region_id=region_id)

@app.route("/register/<region_id>", methods=["GET", "POST"])
def register(region_id):
    if request.method == "POST":
        data = load_data()
        data["records"].append({
            "region": region_id,
            "vehicle": request.form["vehicle"],
            "employee": request.form["employee"],
            "time": datetime.now().strftime("%H:%M")
        })
        save_data(data)
        return redirect(url_for("register", region_id=region_id))
    return render_template("index.html", region_id=region_id)

if __name__ == "__main__":
    app.run(debug=True)
