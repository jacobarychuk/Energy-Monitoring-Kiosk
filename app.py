from flask import Flask, render_template
from w1thermsensor import W1ThermSensor

app = Flask(__name__)

@app.route("/")
def index():
    sensor_data = []
    for sensor in W1ThermSensor.get_available_sensors():
        sensor_data.append({
            "id": sensor.id,
            "temperature": sensor.get_temperature()
        })

    return render_template("index.html", sensors=sensor_data)
