from datetime import datetime, timezone
from math import isfinite

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

LIVE_POLE_ID = "pole-03"

latest_data = {
    "pole_id": LIVE_POLE_ID,
    "temperature": None,
    "humidity": None,
    "received_at": None,
}


def parse_sensor_value(data, name, minimum, maximum):
    value = data.get(name)

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")

    value = float(value)
    if not isfinite(value) or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")

    return value


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/sensor", methods=["POST"])
def receive_sensor():
    global latest_data

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "Expected a JSON object"}), 400

    try:
        temperature = parse_sensor_value(data, "temperature", -40, 80)
        humidity = parse_sensor_value(data, "humidity", 0, 100)
    except ValueError as error:
        return jsonify({"success": False, "error": str(error)}), 400

    latest_data = {
        "pole_id": LIVE_POLE_ID,
        "temperature": temperature,
        "humidity": humidity,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }

    print("Received:", latest_data)

    return jsonify({"success": True, "pole_id": LIVE_POLE_ID})


@app.route("/api/sensor", methods=["GET"])
def get_sensor():
    return jsonify(latest_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
