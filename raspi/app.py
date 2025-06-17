from flask import Flask, render_template, request, jsonify
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

@app.route("/temperature-range")
def temperature_range():
    start = int(request.args.get("start"))
    end = int(request.args.get("end"))

    data = {
        "glycol": [],
        "preheat": [],
        "ambient": [],
        "source": [],
        "hot": []
    }

    with sqlite3.connect("sensor_data.db", isolation_level=None) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT * FROM samples
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp
        """, (start, end))

    for row in cur.fetchall():
        timestamp_ms = row[0] * 1000 # Convert to milliseconds for compatability with Highcharts
        data["glycol"].append([timestamp_ms, row[1]])
        data["preheat"].append([timestamp_ms, row[2]])
        data["ambient"].append([timestamp_ms, row[3]])
        data["source"].append([timestamp_ms, row[4]])
        data["hot"].append([timestamp_ms, row[5]])

    return jsonify(data)
