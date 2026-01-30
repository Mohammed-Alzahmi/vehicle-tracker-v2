from flask import Flask, render_template, request, redirect, url_for
import json
import os
import qrcode
from datetime import datetime
import pytz

app = Flask(__name__)

DATA_FILE = "data.json"
QR_FOLDER = "static/qr"
UAE_TZ = pytz.timezone("Asia/Dubai")

os.makedirs(QR_FOLDER, exist_ok=True)

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
    region = request.form["region"]
    data = load_data()
    if region not in data["regions"]:
        data["regions"][region] = []
        save_data(data)
    return redirect(url_for("home"))

@app.route("/records/<region>")
def records(region):
    data = load_data()
    return render_template(
        "records.html",
        region=region,
        records=data["regions"].get(region, [])
    )

@app.route("/register/<region>", methods=["GET", "POST"])
def register(region):
    if request.method == "POST":
        name = request.form["name"]
        vehicle = request.form["vehicle"]

        now = datetime.now(UAE_TZ).strftime("%H:%M")

        qr_data = f"Region: {region}\nName: {name}\nVehicle: {vehicle}\nTime: {now}"
        qr_img = qrcode.make(qr_data)

        qr_name = f"{region}_{len(os.listdir(QR_FOLDER))}.png"
        qr_path = os.path.join(QR_FOLDER, qr_name)
        qr_img.save(qr_path)

        data = load_data()
        data["regions"][region].append({
            "name": name,
            "vehicle": vehicle,
            "time": now,
            "qr": qr_name
        })
        save_data(data)

        return redirect(url_for("records", region=region))

    return render_template("register.html", region=region)

if __name__ == "__main__":
    app.run(debug=True)
