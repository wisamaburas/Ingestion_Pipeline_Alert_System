# Ingestion Pipeline & Alert System

## Setup
1. Create and activate a virtual environment (if needed)
2. Install dependencies: `pip install flask` (if needed)

## Run
`python3 main.py` (or python main.py)

## Test
Example of sending a reading:

`curl -X POST http://localhost:5000/readings -H "Content-Type: application/json" --data-raw '{"device_id": "CGM-AU-00421", "patient_id": "PT-8812", "reading": {"glucose_mgdl": 187.4, "battery_pct": 62, "signal_quality": "good", "recorded_at": "2025-11-03T14:22:05Z"}}'`

Example of a patient query, where n = 4:

`curl "http://localhost:5000/patients/PT-8812/summary?n=4"`
