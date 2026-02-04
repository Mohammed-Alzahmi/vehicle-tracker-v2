from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os
import pytz

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"regions": {}}
    with open(DATA_FILE, "r", encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", regions=data["regions"])

@app.route("/region/<name>")
def region_details(name):
    data = load_data()
    region_data = data["regions"].get(name, {"records": [], "car_types": ["دورية", "مدني"]})
    return render_template("region_details.html", region=name, records=region_data["records"], car_types=region_data.get("car_types", ["دورية", "مدني"]))

@app.route("/add-region", methods=["POST"])
def add_region():
    region = request.form["region"]
    data = load_data()
    if region and region not in data["regions"]:
        data["regions"][region] = {"records": [], "car_types": ["دورية", "مدني"]}
        save_data(data)
    return redirect(url_for("index"))

@app.route("/manage-cars", methods=["POST"])
def manage_cars():
    data = load_data()
    region = request.json["region"]
    action = request.json["action"]
    value = request.json["value"]
    
    if region in data["regions"]:
        if "car_types" not in data["regions"][region]:
            data["regions"][region]["car_types"] = ["دورية", "مدني"]
            
        if action == "add" and value not in data["regions"][region]["car_types"]:
            data["regions"][region]["car_types"].append(value)
        elif action == "delete":
            data["regions"][region]["car_types"].remove(value)
        save_data(data)
    return jsonify(success=True)

@app.route("/register/<region>", methods=["GET", "POST"])
def register_entry(region):
    data = load_data()
    if request.method == "POST":
        try:
            uae_tz = pytz.timezone('Asia/Dubai')
            now = datetime.now(uae_tz)
            new_record = {
                "name": request.form["name"],
                "military_id": request.form["military_id"],
                "car_type": request.form["car_type"],
                "time": now.strftime("%Y-%m-%d | %I:%M %p"),
                "id": str(now.timestamp())
            }
            data["regions"][region]["records"].insert(0, new_record)
            save_data(data)
            return render_template("success.html", region=region)
        except Exception as e:
            return f"Error: {str(e)}", 500
            
    car_types = data["regions"].get(region, {}).get("car_types", ["دورية", "مدني"])
    return render_template("register.html", region=region, car_types=car_types)

# باقي الـ Routes (حذف، تعديل) تبقى كما هي بس تأكدي من مسار data["regions"][name]["records"]