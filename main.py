# task 1

from flask import Flask, request, jsonify
from database import init_db, insert_reading, DuplicateReadingError
 
app = Flask(__name__)
init_db()

class Payload:
    valid_signal_quality = {"good", "poor", "degraded"}

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
    except DuplicateReadingError:
        return jsonify({"status": "duplicate"}), 409
 
    return jsonify({"status": "accepted"}), 201
 
 
if __name__ == "__main__":
    app.run(debug=True, port=5000)