import sqlite3
 
DB_NAME = "readings.db"
 
 
class DuplicateReadingError(Exception):
    pass
 
 
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            device_id      TEXT,
            patient_id     TEXT,
            glucose_mgdl   REAL,
            battery_pct    REAL,
            signal_quality TEXT,
            recorded_at    TEXT,
            PRIMARY KEY (device_id, recorded_at)
        )
    """)
    conn.commit()
    conn.close()
 
 
def insert_reading(reading: dict):
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute("""
            INSERT INTO readings VALUES
            (:device_id, :patient_id, :glucose_mgdl, :battery_pct, :signal_quality, :recorded_at)
        """, reading)
        conn.commit()
    except sqlite3.IntegrityError:
        raise DuplicateReadingError()
    finally:
        conn.close()

# cx = sqlite3.connect("test.db")

# cx = sqlite3.connect(":memory:")


# cu = cx.cursor()


# # create a table
# cu.execute("create table lang(name, first_appeared)")
# cu.execute("create table validate(device_id, patient_id, glucose_mgdl, battery_pct, signal_quality, recorded_at)")


# # insert values into a table
# cu.execute("insert into validate values (?, ?)", ("C", 1972))


# # execute a query and iterate over the result
# for row in cu.execute("select * from validate"):
#         print(row)
# cx.close()

