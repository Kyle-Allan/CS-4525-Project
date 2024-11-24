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


cursor.execute("""
select * from Temperature
""")

rows = cursor.fetchall()

# Print results
for row in rows:
    print(row)


# Close the connection
conn.close()
