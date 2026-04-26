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
o	}


- Patients may have individual threshold configurations (e.g diabetic has tighter bounds)

Task 01:

- Class diagram attached
- SQLite chosen as database management as it can store databases as a single file, matching the criteria of the task whilst also allowing for simplified database updating/accessing

Task 02: 

- Threshold: 70 mg/dL (low) - 180 mg/dL (high)
- Diabetes threshold: 80 - 160
- Critically high diabetes: > 220 (own decision)
- Critically low diabetes : < 40 (own decision)
- Low battery percentage alert : < 20 (own decision)
- Signal quality low alert : when degraded 
- Warn if database is no longer being updated each 5 mins (time constraint limit reached)

Task 03:

GET request: 

- needs to filter sqllite by patient id, n specified
- returns n rows, 
- most recent alerts, (time constraint limit reached)
- battery/signal health, 
- time-in-range-percentage (time constraint limit reached)

Task 04:

Already handled different arrival times in task 3 with the 'ORDER BY' constraint. this outputs query readings in the order of most recent to least recent times. This is better than a simple append only model as late arrivals can go into the correct positions.

However, a constraint that could not be fixed in the time limit is that any date can be parsed through even if it is not in the correct format. this means that currently if there is an incorrect time, it disrupts the order of the database output. Could be fixed in the future with a check in place that checks if 
date format is correct, and returns http error if it is not. 


Assumptions made:

A few assumptions were made. I assumed the critically high/low glucose limits based on some quick research online, and assumed 409 error for duplicate (actual 409 is conflict, chose it due to belief that it was most applicable).

Data model:

Storage was structured in a readings table created with sqllite. has the primary key set to device_id, recorded_at, meaning that the device id cant have the same recorded at time in multiple rows. This is how the duplicate method was integrated as an easier way to catch it quicker. The glucose threshold per patient was stored as a dictionary rather than a seperate table in sqllite due to time constraints

Alerting strategy:

Could use a ticket-like system. if an alert is linked to reading, raise a ticket. once new reading is taken after 5 mins and the alert has been fixed, could close ticket. can assign levels of priority for each ticket, higher number could indicate higher priority, useful for my added 'critically low' values, helps determine who needs help the most. in current practice I just printed out alerts without adding these features due to time constraints, but at a higher scale could use a more in depth database system (eg. mySQL), where each patient can be listed as seperate entries in the database, can have a row specific for no.Tickets to track how many alerts/tickets the patient has, and that can link to seperate table that determines the ticket priority across all patients in system. 

Trade offs:

1. Used a dictionary for the patient with diabetes instead of adding a new patients table in the database, was done due to time constraints 

2. the order by method used for part 4 is only good in a smaller scale as it has to check all database entries, was done this way as this is not a full scale system and works for boundaries of the task. 

What would be changed with more time:

- Add ticketed alerts idea to seperate database table
- Ensure timestamp / other inputs are correct format before being pushed to database
- Implement alerts output, time-in-percentage, and no database update warning system
- Add a proper testing document instead of testing via terminal curl commands