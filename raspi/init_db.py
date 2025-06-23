import sqlite3

with sqlite3.connect("sensor_data.db", isolation_level=None) as con:
    cur = con.cursor() # Used to execute SQL statements and fetch results from SQL queries
    cur.execute("""
        CREATE TABLE IF NOT EXISTS samples (
            timestamp INTEGER PRIMARY KEY,
            glycol REAL NOT NULL,
            preheat REAL NOT NULL,
            ambient REAL NOT NULL,
            source REAL NOT NULL,
            hot REAL NOT NULL,
            flow REAL NOT NULL
        ) STRICT
    """)
