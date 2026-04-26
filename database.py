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

def get_reading(patient_id, n=12):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM readings WHERE patient_id = ? ORDER BY recorded_at DESC LIMIT ?", (patient_id, n))
    result = cur.fetchmany(n)
    conn.close()
    return result

