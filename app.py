from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"

# ---------- Data ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"regions": {}}, f, ensure_ascii=False, indent=4)

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
    name = request.form["region"].strip()
    data = load_data()

    if name and name not in data["regions"]:
        data["regions"][name] = {"logs": []}
        save_data(data)

    return redirect(url_for("home"))


@app.route("/region/<name>")
def region_details(name):
    data = load_data()
    return render_template(
        "region_details.html",
        region=name,
        logs=data["regions"][name]["logs"]
    )


@app.route("/qr")
def qr_view():
    return render_template("qr_view.html", region=request.args.get("region"))


@app.route("/register", methods=["POST"])
def register():
    data = load_data()

    region = request.form["region"]
    employee = request.form["employee"]
    vehicle = request.form["vehicle"]

    # UAE Time (UTC +4)
    uae_time = datetime.utcnow() + timedelta(hours=4)
    time_str = uae_time.strftime("%Y-%m-%d %H:%M")  # 24-hour

    data["regions"][region]["logs"].append({
        "employee": employee,
        "vehicle": vehicle,
        "time": time_str
    })

    save_data(data)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run()
