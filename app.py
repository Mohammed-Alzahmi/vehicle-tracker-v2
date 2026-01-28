from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "database.db"

# ---------- Database ----------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE regions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        conn.execute("""
            CREATE TABLE records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region_id INTEGER,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (region_id) REFERENCES regions (id)
            )
        """)
        conn.commit()
        conn.close()

init_db()

# ---------- Routes ----------
@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()

    if request.method == "POST":
        region_name = request.form.get("region")
        if region_name:
            try:
                conn.execute(
                    "INSERT INTO regions (name) VALUES (?)",
                    (region_name,)
                )
                conn.commit()
            except:
                pass
        conn.close()
        return redirect(url_for("index"))

    regions = conn.execute("SELECT * FROM regions").fetchall()
    conn.close()
    return render_template("index.html", regions=regions)

@app.route("/region/<int:region_id>", methods=["GET", "POST"])
def region_details(region_id):
    conn = get_db_connection()

    region = conn.execute(
        "SELECT * FROM regions WHERE id = ?",
        (region_id,)
    ).fetchone()

    if not region:
        conn.close()
        return "Region not found", 404

    if request.method == "POST":
        note = request.form.get("note")
        if note:
            conn.execute(
                "INSERT INTO records (region_id, note) VALUES (?, ?)",
                (region_id, note)
            )
            conn.commit()
        return redirect(url_for("region_details", region_id=region_id))

    records = conn.execute(
        "SELECT * FROM records WHERE region_id = ? ORDER BY created_at DESC",
        (region_id,)
    ).fetchall()

    conn.close()
    return render_template(
        "region_details.html",
        region=region,
        records=records
    )

if __name__ == "__main__":
    app.run(debug=True)
