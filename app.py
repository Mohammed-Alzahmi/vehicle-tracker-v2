from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os
import pytz

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"regions": {}, "car_types": []} # قائمة السيارات تبدأ فاضية
    with open(DATA_FILE, "r", encoding='utf-8') as f:
        data = json.load(f)
        if "car_types" not in data: data["car_types"] = []
        return data

def save_data(data):
    with open(DATA_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", regions=data["regions"])

@app.route("/register/<region>", methods=["GET", "POST"])
def register_entry(region):
    data = load_data()
    if request.method == "POST":
        uae_tz = pytz.timezone('Asia/Dubai')
        now = datetime.now(uae_tz)
        new_record = {
            "name": request.form["name"],
            "military_id": request.form["military_id"],
            "car_type": request.form["car_type"],
            "time": now.strftime("%Y-%m-%d | %I:%M %p"),
            "id": str(now.timestamp())
        }
        if region not in data["regions"]: data["regions"][region] = []
        data["regions"][region].insert(0, new_record)
        save_data(data)
        return render_template("success.html", region=region)
    return render_template("register.html", region=region, car_types=data["car_types"])

@app.route("/region/<name>")
def region_details(name):
    data = load_data()
    return render_template("region_details.html", region=name, records=data["regions"].get(name, []), car_types=data["car_types"])

@app.route("/add-region", methods=["POST"])
def add_region():
    region = request.form["region"]
    data = load_data()
    if region not in data["regions"]:
        data["regions"][region] = []
        save_data(data)
    return redirect(url_for("index"))

@app.route("/delete-records", methods=["POST"])
def delete_records():
    data = load_data()
    region, ids = request.json["region"], request.json["ids"]
    if region in data["regions"]:
        data["regions"][region] = [r for r in data["regions"][region] if r["id"] not in ids]
        save_data(data)
    return jsonify(success=True)

@app.route("/manage-cars", methods=["POST"])
def manage_cars():
    data = load_data()
    action, value = request.json["action"], request.json["value"]
    if action == "add" and value not in data["car_types"]: data["car_types"].append(value)
    elif action == "delete" and value in data["car_types"]: data["car_types"].remove(value)
    save_data(data)
    return jsonify(success=True)

@app.route("/edit-region", methods=["POST"])
def edit_region():
    data = load_data()
    old, new = request.json["old"], request.json["new"]
    if old in data["regions"]:
        data["regions"][new] = data["regions"].pop(old)
        save_data(data)
    return jsonify(success=True)

@app.route("/delete-region", methods=["POST"])
def delete_region():
    data = load_data()
    name = request.json["name"]
    if name in data["regions"]:
        del data["regions"][name]
        save_data(data)
    return jsonify(success=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)