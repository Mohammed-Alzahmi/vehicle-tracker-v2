from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# ---------- Helpers ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"regions": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---------- Routes ----------
@app.route("/")
def home():
    data = load_data()
    return render_template("home.html", regions=data["regions"])

@app.route("/add_region", methods=["POST"])
def add_region():
    region_name = request.form["region"]
    data = load_data()

    if region_name not in data["regions"]:
        data["regions"][region_name] = {
            "logs": []
        }

    save_data(data)
    return redirect(url_for("home"))

@app.route("/region/<region_name>")
def region_details(region_name):
    data = load_data()
    region = data["regions"].get(region_name)

    if not region:
        return "Region not found", 404

    return render_template(
        "region_details.html",
        region_name=region_name,
        logs=region["logs"]
    )

@app.route("/qr")
def qr_view():
    region_name = request.args.get("region")
    return render_template("qr_view.html", region_name=region_name)

@app.route("/register", methods=["POST"])
def register():
    region_name = request.form["region"]
    employee = request.form["employee"]
    vehicle = request.form["vehicle"]

    data = load_data()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    log = {
        "employee": employee,
        "vehicle": vehicle,
        "time": now
    }

    data["regions"][region_name]["logs"].append(log)
    save_data(data)

    return jsonify({"status": "success"})

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
