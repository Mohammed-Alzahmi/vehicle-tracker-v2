from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os
import pytz

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE): return {"regions": {}}
    with open(DATA_FILE, "r", encoding='utf-8') as f: return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", regions=data["regions"])

@app.route("/region/<name>")
def region_details(name):
    data = load_data()
    region_data = data["regions"].get(name, {"records": [], "car_types": []})
    return render_template("region_details.html", region=name, records=region_data["records"], car_types=region_data.get("car_types", []))

@app.route("/add-region", methods=["POST"])
def add_region():
    region = request.form["region"]
    data = load_data()
    if region and region not in data["regions"]:
        data["regions"][region] = {"records": [], "car_types": []}
        save_data(data)
    return redirect(url_for("index"))

@app.route("/edit-region", methods=["POST"])
def edit_region():
    data = load_data()
    old_n, new_n = request.json["old"], request.json["new"]
    if old_n in data["regions"]:
        data["regions"][new_n] = data["regions"].pop(old_n)
        save_data(data)
    return jsonify(success=True)

@app.route("/delete-region", methods=["POST"])
def delete_region():
    data = load_data()
    if request.json["name"] in data["regions"]:
        del data["regions"][request.json["name"]]
        save_data(data)
    return jsonify(success=True)

@app.route("/manage-cars", methods=["POST"])
def manage_cars():
    data = load_data()
    region, action, value = request.json["region"], request.json["action"], request.json["value"]
    if region in data["regions"]:
        if "car_types" not in data["regions"][region]: data["regions"][region]["car_types"] = []
        if action == "add": data["regions"][region]["car_types"].append(value)
        elif action == "delete": data["regions"][region]["car_types"].remove(value)
        save_data(data)
    return jsonify(success=True)

@app.route("/delete-records", methods=["POST"])
def delete_records():
    data = load_data()
    region, ids = request.json["region"], request.json["ids"]
    data["regions"][region]["records"] = [r for r in data["regions"][region]["records"] if r["id"] not in ids]
    save_data(data)
    return jsonify(success=True)