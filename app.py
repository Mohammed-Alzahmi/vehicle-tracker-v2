from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"regions": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", regions=data["regions"])

@app.route("/add-region", methods=["POST"])
def add_region():
    region = request.form["region"]
    data = load_data()
    if region not in data["regions"]:
        data["regions"][region] = []
        save_data(data)
    return redirect(url_for("index"))

@app.route("/region/<name>")
def region_details(name):
    data = load_data()
    records = data["regions"].get(name, [])
    return render_template("region_details.html", region=name, records=records)

@app.route("/delete-region", methods=["POST"])
def delete_region():
    data = load_data()
    name = request.json["name"]
    if name in data["regions"]:
        del data["regions"][name]
        save_data(data)
    return jsonify(success=True)

@app.route("/edit-region", methods=["POST"])
def edit_region():
    data = load_data()
    old = request.json["old"]
    new = request.json["new"]
    if old in data["regions"]:
        data["regions"][new] = data["regions"].pop(old)
        save_data(data)
    return jsonify(success=True)

@app.route("/qr/<region>")
def qr_view(region):
    return render_template("qr_view.html", region=region)

if __name__ == "__main__":
    app.run(debug=True)
