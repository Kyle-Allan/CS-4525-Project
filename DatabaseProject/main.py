import sqlite3

# Connect to SQLite
conn = sqlite3.connect("time_series.db")  # Creates the .db file
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Temperature (
    Time DATETIME NOT NULL,          -- Records time accurate to seconds
    Temperature REAL NOT NULL,       -- Records temperature to two decimal points
    PRIMARY KEY (Time, Temperature)     -- Ensures uniqueness of Time and DeviceID
)
""")
conn.commit()


'''
# Insert sample data stream
data_stream = [
    ('2024-11-22 12:03:00', 4),
    ('2024-11-22 12:04:00', 5),
    ('2024-11-22 12:05:00', 6)
]

cursor.executemany("""
INSERT INTO Temperature (Time, Temperature)
VALUES (?, ?)
""", data_stream)
conn.commit()
'''


# Search for a specific timestamp
timestamp = '2024-11-22 12:00:00'
cursor.execute("SELECT * FROM Temperature WHERE Time = ?", (timestamp,))
result = cursor.fetchall()
print('Exact Time')
print(result)

# Range query
start_time = '2024-11-22 12:00:00'
end_time = '2024-11-22 12:10:00'
cursor.execute("""
SELECT * FROM Temperature
WHERE Time BETWEEN ? AND ?
""", (start_time, end_time))
results = cursor.fetchall()

print('Range')
for row in results:
    print(row)

# Close the connection
conn.close()
