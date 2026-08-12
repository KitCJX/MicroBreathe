from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

latest_data = {"temperature": None, "humidity": None}


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/sensor", methods=["POST"])
def receive_sensor():
    global latest_data

    data = request.get_json()

    latest_data = {
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
    }

    print("Received:", latest_data)

    return jsonify({"success": True})


@app.route("/api/sensor", methods=["GET"])
def get_sensor():
    return jsonify(latest_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
