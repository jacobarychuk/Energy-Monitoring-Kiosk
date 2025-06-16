from flask import Flask, render_template, request

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
    return "OK"
