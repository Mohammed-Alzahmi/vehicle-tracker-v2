from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os
import qrcode

app = Flask(__name__)

DATA_FILE = "data.json"

# -----------------------------
# Load & Save Data
# -----------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"regions": [], "logs": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# -----------------------------
# Dashboard
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    data = load_data()

    if request.method == "POST":
        region = request.form.get("data")
        if region and region not in data["regions"]:
            data["regions"].append(region)
            data["logs"][region] = []

            # Generate QR
            qr_link = request.url_root + "register?region=" + region
            qr_img = qrcode.make(qr_link)
            qr_img.save(f"static/qr_{region}.png")

            save_data(data)

    return render_template("home.html", regions=data["regions"])

# -----------------------------
# Delete Region
# -----------------------------
@app.route("/delete/<region>")
def delete_region(region):
    data = load_data()
    if region in data["regions"]:
        data["regions"].remove(region)
        data["logs"].pop(region, None)
        qr_path = f"static/qr_{region}.png"
        if os.path.exists(qr_path):
            os.remove(qr_path)
        save_data(data)
    return redirect(url_for("home"))

# -----------------------------
# Region Details
# -----------------------------
@app.route("/view/<region>")
def view_region(region):
    data = load_data()
    if region not in data["regions"]:
        return redirect(url_for("home"))

    return render_template(
        "qr_view.html",
        region=region,
        logs=data["logs"].get(region, []),
        qr_filename=f"qr_{region}.png"
    )

# -----------------------------
# Registration Page
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    data = load_data()
    success = False
    region = request.args.get("region")

    if request.method == "POST":
        employee = request.form.get("employee")
        if employee and region in data["logs"]:
            data["logs"][region].append({
                "name": employee,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_data(data)
            success = True

    return render_template("index.html", success=success)
