from flask import Flask, request, jsonify
from database import init_db, insert_reading, get_reading, DuplicateReadingError
 
app = Flask(__name__)
init_db()

mgdl_threshold = { 
    "PT-8813": (80, 160), # diabetes
    }

default_threshold = (70, 180)

class Payload:
    valid_signal_quality = {"good", "poor", "degraded"}
    valid_theshold = {}

    def __init__(self, data: dict):
        self.device_id = data.get("device_id")
        self.patient_id = data.get("patient_id")

        reading = data.get("reading", {})
        self.glucose_mgdl = reading.get("glucose_mgdl")
        self.battery_pct = reading.get("battery_pct")
        self.signal_quality = reading.get("signal_quality")
        self.recorded_at = reading.get("recorded_at")

        self.validate()

    def validate(self):
        if not self.device_id:
            raise ValueError("device_id required")

        if not self.patient_id:
            raise ValueError("patient_id required")

        if self.signal_quality not in self.valid_signal_quality:
            raise ValueError("invalid signal_quality")

        if self.glucose_mgdl is None or self.glucose_mgdl < 0:
            raise ValueError("invalid glucose_mgdl")

        if self.battery_pct is None or not (0 <= self.battery_pct <= 100):
            raise ValueError("battery_pct must be 0-100")

        if not self.recorded_at:
            raise ValueError("recorded_at required")
        


@app.route("/readings", methods=["POST"])
def ingest_reading():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "invalid JSON"}), 400
 
    try:
        payload = Payload(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
 
    reading = {
        "device_id": payload.device_id,
        "patient_id": payload.patient_id,
        "glucose_mgdl": payload.glucose_mgdl,
        "battery_pct": payload.battery_pct,
        "signal_quality": payload.signal_quality,
        "recorded_at": payload.recorded_at,
    }
 
    try:
        insert_reading(reading)

        low, high = mgdl_threshold.get(payload.patient_id, default_threshold) # use default if patient not found
        if payload.glucose_mgdl < low or payload.glucose_mgdl > high: 
            print(f"Alert: {payload.patient_id} glucose {payload.glucose_mgdl} out of range ({low}-{high})")
        if payload.glucose_mgdl < 40:
            print(f"Alert: {payload.patient_id} glucose {payload.glucose_mgdl} is critically low")
        if payload.glucose_mgdl > 220:
            print(f"Alert: {payload.patient_id} glucose {payload.glucose_mgdl} is critically high")
        if payload.battery_pct < 20:
            print(f"Alert: {payload.patient_id} battery {payload.battery_pct} is low")
        if payload.signal_quality == "degraded":
            print(f"Alert: {payload.patient_id} signal quality is {payload.signal_quality}")
    except DuplicateReadingError:
        return jsonify({"status": "duplicate"}), 409
 
    return jsonify({"status": "accepted"}), 201
 
 
@app.route("/patients/<patient_id>/summary", methods=["GET"])
def get_summary(patient_id):
    n = request.args.get("n", 12, type=int)
    readings = get_reading(patient_id, n)
    latest = readings[0] if readings else None
    return jsonify({
        "readings": readings,
        "battery_pct": latest[3] if latest else None,
        "signal_quality": latest[4] if latest else None,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)