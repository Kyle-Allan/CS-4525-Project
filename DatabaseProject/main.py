import sqlite3

# Connect to SQLite
conn = sqlite3.connect("time_series.db")  # Creates the .db file
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Temperature (
    Time DATETIME NOT NULL,          -- Records time accurate to seconds
    Temperature REAL NOT NULL,       -- Records temperature to two decimal points
    DeviceID TEXT NOT NULL,          -- Unique identifier for the device
    PRIMARY KEY (Time, DeviceID)     -- Ensures uniqueness of Time and DeviceID
)
""")
conn.commit()

# Insert sample data
# Insert sample data stream
data_stream = [
    ('2024-11-22 12:01:00', 22.55, '1'),
    ('2024-11-22 12:05:00', 23.10, '2'),
    ('2024-11-22 12:10:00', 21.95, '1')
]

cursor.executemany("""
INSERT INTO Temperature (Time, Temperature, DeviceID)
VALUES (?, ?, ?)
""", data_stream)
conn.commit()

# Close the connection
conn.close()
