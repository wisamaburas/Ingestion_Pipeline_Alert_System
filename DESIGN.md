Goal:

Data ingestion and alerting system. Continuous glucose monitoring at regular intervals and system recieves, process, stores. Raises alerts when readings cross clinical thresholds.

Specifications:
-	Reading every 5 mins via HTTP endpoint
o	Glucose level (mg/dL)
o	Device ID
o	Patient ID
o	Battery %
o	Signal quality

Example:
o	Timestamp Base payload model design
o	{
o	"device_id": "CGM-AU-00421",
o	"patient_id": "PT-8812",
o	"reading": {
o	"glucose_mgdl": 187.4,
o	"battery_pct": 62,
o	"signal_quality": "good", // "good" | "poor" | "degraded"
o	"recorded_at": "2025-11-03T14:22:05Z"
o	}
o	}ps


- Patients may have individual threshold configurations (e.g diabetic has tighter bounds)

Task 01:

- Class diagram attached

Task 02: 

