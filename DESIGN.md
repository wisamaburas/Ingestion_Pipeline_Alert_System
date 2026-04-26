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

- Threshold: 70 mg/dL (low) - 180 mg/dL (high)
- Diabetes threshold: 80 - 160
- Critically high diabetes: > 220 (own decision)
- Critically low diabetes : < 40 (own decision)
- Low battery percentage alert : < 20 (own decision)
- Signal quality low alert : when degraded 
- Warn if database is no longer being updated each 5 mins (time constraint limit)

Task 03:

GET request: 

- needs to filter sqllite by patient id, n specified
- returns n rows, most recent alerts, battery/signal health, time-in-range-percentage


Alerting strategy:

Could use a ticket-like system. if an alert is linked to reading, raise a ticket. once new reading is taken after 5 mins and the alert has been fixed, could close ticket. can assign levels of priority for each ticket, higher number could indicate higher priority, useful for my added 'critically low' values, helps determine who needs help the most. in current practice I just printed out alerts without adding these features due to time constraints, but at a higher scale could use a more in depth database system (eg. mySQL), where each patient can be listed as seperate entries in the database, can have a row specific for no.Tickets to track how many alerts/tickets the patient has, and that can link to seperate table that determines the ticket priority across all patients in system. 

