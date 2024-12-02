import sqlite3
import csv
import time  # Import the time module

# Connect to SQLite
conn = sqlite3.connect("time_series.db")  # Creates the .db file
cursor = conn.cursor()

'''
cursor.execute("""Drop table if exists Temperature""")
conn.commit()
'''

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Temperature (
    Time DATETIME NOT NULL,          -- Records time accurate to seconds
    Temperature REAL NOT NULL,       -- Records temperature to two decimal points
    PRIMARY KEY (Time, Temperature)     -- Ensures uniqueness of Time and Temperature
)
""")
conn.commit()


'''
# Insert data from CSV
with open("data_150000.csv", mode="r") as file:
    reader = csv.DictReader(file)
    # Measure insertion time
    start_time = time.time()  # Start the timer
    for row in reader:
        cursor.execute("INSERT INTO Temperature (Time, Temperature) VALUES (?, ?)", (row["time"], row["temperature"]))

conn.commit()  # Commit changes to the database
end_time = time.time()  # Stop the timer
print(f"SQL populated with 150 000 rows in {end_time - start_time:.2f} seconds.")
'''

# Search for a specific timestamp
timestamp = '2024-01-01T02:18:12'
cursor.execute("SELECT * FROM Temperature WHERE Time = ?", (timestamp,))
result = cursor.fetchall()
print('Exact Time')
print(result)

# Define the range
start_time = "2024-01-01T00:00:00"
end_time = "2024-01-03T00:00:00"

# Measure query execution time
start = time.time()
cursor.execute("SELECT * FROM Temperature WHERE Time BETWEEN ? AND ?", (start_time, end_time))
results = cursor.fetchall()
end = time.time()

# Print the results and timing
print(f"SQL Range Query retrieved {len(results)} rows in {end - start:.2f} seconds.")
conn.close()
