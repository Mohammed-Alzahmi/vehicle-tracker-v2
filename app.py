from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# Data Storage (Temporary)
# -----------------------------
regions = []
logs = {}

# -----------------------------
# Dashboard (Home Page)
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.form.get("data")
        if data and data not in regions:
            regions.append(data)
            logs[data] = []
    return render_template("home.html", regions=regions)


# -----------------------------
# Delete Region
# -----------------------------
@app.route("/delete/<region>")
def delete_region(region):
    if region in regions:
        regions.remove(region)
        logs.pop(region, None)
    return redirect(url_for("home"))


# -----------------------------
# Region Details (QR + Logs)
# -----------------------------
@app.route("/view/<region>")
def view_region(region):
    if region not in regions:
        return redirect(url_for("home"))

    qr_filename = "qr.png"  # placeholder (if you generate dynamically later)
    return render_template(
        "qr_view.html",
        region=region,
        logs=logs.get(region, []),
        qr_filename=qr_filename
    )


# -----------------------------
# Registration Page (Employee Entry)
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    success = False
    if request.method == "POST":
        employee = request.form.get("employee")
        region = request.args.get("region")

        if employee and region and region in logs:
            logs[region].append({
                "name": employee,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            success = True

    return render_template("index.html", success=success)


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
