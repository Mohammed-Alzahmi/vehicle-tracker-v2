from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# تخزين مؤقت (بعدين نحولها DB)
regions = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        region_name = request.form.get("region")
        if region_name:
            regions.append(region_name)
        return redirect(url_for("index"))

    return render_template("index.html", regions=regions)

@app.route("/region/<name>")
def region_details(name):
    return render_template("region_details.html", region=name)

if __name__ == "__main__":
    app.run(debug=True)
