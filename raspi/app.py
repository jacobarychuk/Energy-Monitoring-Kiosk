from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Web interface
@app.route("/")
def index():
    return render_template("index.html")

# ESP32 sends data here
@app.route("/data", methods=["POST"])
def receive_data():
    content = request.get_json()
    print("Received:", content)

    # Extract expected fields
    expected_fields = ["timestamp", "glycol", "preheat", "ambient", "source", "hot"]
    if not all(key in content for key in expected_fields):
        return 400

    # Insert into database
    with sqlite3.connect("sensor_data.db", isolation_level=None) as con:
        cur = con.cursor() # Used to execute SQL statements and fetch results from SQL queries
        cur.execute("""
            INSERT INTO samples (timestamp, glycol, preheat, ambient, source, hot)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            content["timestamp"],
            content["glycol"],
            content["preheat"],
            content["ambient"],
            content["source"],
            content["hot"]
        ))

    return "OK"
