from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import os
import pytz
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# رابط السوبابيس الحقيقي مالج - مكتوب مرة وحدة بس عشان ما يستوي إيرور
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Moh317632m%40%40db.zsscaqtbfasrseodhwbt.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------- جداول الداتا بيس -----------------

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    car_types = db.relationship('CarType', backref='region', lazy=True, cascade="all, delete-orphan")
    records = db.relationship('VehicleRecord', backref='region', lazy=True, cascade="all, delete-orphan")

class CarType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)

class VehicleRecord(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    military_id = db.Column(db.String(50), nullable=False)
    car_type = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)

with app.app_context():
    db.create_all()

# ----------------- الطرق (Routes) -----------------

@app.route("/")
def index():
    regions = Region.query.all()
    regions_dict = {r.name: {} for r in regions}
    return render_template("index.html", regions=regions_dict)

@app.route("/region/<name>")
def region_details(name):
    region = Region.query.filter_by(name=name).first_or_404()
    records_list = [{
        "id": r.id,
        "name": r.name,
        "military_id": r.military_id,
        "car_type": r.car_type,
        "time": r.time
    } for r in region.records]
    
    records_list.reverse()
    car_types_list = [c.name for c in region.car_types]
    return render_template("region_details.html", region=name, records=records_list, car_types=car_types_list)

@app.route("/qr/<region>")
def view_qr(region):
    return render_template("qr_view.html", region_id=region)

@app.route("/add-region", methods=["POST"])
def add_region():
    region_name = request.form["region"].strip()
    if region_name:
        existing = Region.query.filter_by(name=region_name).first()
        if not existing:
            new_reg = Region(name=region_name)
            db.session.add(new_reg)
            db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit-region", methods=["POST"])
def edit_region():
    old_n = request.json["old"].strip()
    new_n = request.json["new"].strip()
    region = Region.query.filter_by(name=old_n).first()
    if region and not Region.query.filter_by(name=new_n).first():
        region.name = new_n
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 400

@app.route("/delete-region", methods=["POST"])
def delete_region():
    name = request.json["name"]
    region = Region.query.filter_by(name=name).first()
    if region:
        db.session.delete(region)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 400

@app.route("/manage-cars", methods=["POST"])
def manage_cars():
    region_name = request.json["region"]
    action = request.json["action"]
    value = request.json["value"].strip()
    
    region = Region.query.filter_by(name=region_name).first()
    if region:
        if action == "add" and value:
            existing_car = CarType.query.filter_by(name=value, region_id=region.id).first()
            if not existing_car:
                new_car = CarType(name=value, region=region)
                db.session.add(new_car)
        elif action == "delete" and value:
            car_to_del = CarType.query.filter_by(name=value, region_id=region.id).first()
            if car_to_del:
                db.session.delete(car_to_del)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 400

@app.route("/delete-records", methods=["POST"])
def delete_records():
    ids = request.json["ids"]
    for record_id in ids:
        rec = VehicleRecord.query.get(record_id)
        if rec:
            db.session.delete(rec)
    db.session.commit()
    return jsonify(success=True)

@app.route("/register/<region>", methods=["GET", "POST"])
def register_entry(region):
    region_obj = Region.query.filter_by(name=region).first_or_404()
    if request.method == "POST":
        uae_tz = pytz.timezone('Asia/Dubai')
        now = datetime.now(uae_tz)
        
        new_record = VehicleRecord(
            id=str(now.timestamp()),
            name=request.form["name"],
            military_id=request.form["military_id"],
            car_type=request.form["car_type"],
            time=now.strftime("%Y-%m-%d | %I:%M %p"),
            region=region_obj
        )
        db.session.add(new_record)
        db.session.commit()
        return render_template("success.html", region=region)
        
    car_types_list = [c.name for c in region_obj.car_types]
    return render_template("register.html", region=region, car_types=car_types_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))