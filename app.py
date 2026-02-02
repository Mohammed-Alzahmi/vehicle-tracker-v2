from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os
import pytz

app = Flask(__name__)

DATA_FILE = "data.json"

# --- دوال مساعدة ---
# في دالة load_data عدلي هذا الجزء بس عشان تبدأ القائمة فاضية
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

def get_uae_time():
    tz = pytz.timezone('Asia/Dubai')
    return datetime.now(tz).strftime("%Y-%m-%d | %I:%M %p")

# --- الصفحات الرئيسية ---
@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", regions=data["regions"])

# صفحة التسجيل (اللي تطلع لما تسوين سكان)
@app.route("/register/<region>", methods=["GET", "POST"])
def register_entry(region):
    data = load_data()
    if request.method == "POST":
        # حفظ البيانات
        new_record = {
            "name": request.form["name"],
            "military_id": request.form["military_id"],
            "car_type": request.form["car_type"],
            "time": get_uae_time(),
            "id": str(datetime.now().timestamp()) # رقم مميز للحذف
        }
        # تأكد ان المنطقة موجودة
        if region in data["regions"]:
            data["regions"][region].insert(0, new_record) # ضيف في البداية
        else:
            data["regions"][region] = [new_record]
        
        save_data(data)
        return render_template("success.html", region=region) # صفحة شكرا
    
    return render_template("register.html", region=region, car_types=data["car_types"])

# صفحة السجلات (حق الأدمن)
@app.route("/region/<name>")
def region_details(name):
    data = load_data()
    records = data["regions"].get(name, [])
    return render_template("region_details.html", region=name, records=records, car_types=data["car_types"])

# --- API Functions (إدارة الداتا) ---

@app.route("/add-region", methods=["POST"])
def add_region():
    region = request.form["region"]
    data = load_data()
    if region not in data["regions"]:
        data["regions"][region] = []
        save_data(data)
    return redirect(url_for("index"))

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

# حذف السجلات (واحد أو الكل)
@app.route("/delete-records", methods=["POST"])
def delete_records():
    data = load_data()
    region = request.json["region"]
    ids_to_delete = request.json["ids"] # ليستة بالأرقام
    
    if region in data["regions"]:
        # احفظ بس اللي مب موجودين في ليستة الحذف
        data["regions"][region] = [r for r in data["regions"][region] if r["id"] not in ids_to_delete]
        save_data(data)
        
    return jsonify(success=True)

# إدارة أنواع السيارات
@app.route("/manage-cars", methods=["POST"])
def manage_cars():
    data = load_data()
    action = request.json["action"] # add OR delete
    value = request.json["value"]
    
    if action == "add" and value not in data["car_types"]:
        data["car_types"].append(value)
    elif action == "delete" and value in data["car_types"]:
        data["car_types"].remove(value)
        
    save_data(data)
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)



if __name__ == "__main__":
    # هذا التعديل ضروري عشان يشتغل على Render بدون مشاكل
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)