import sqlite3
import csv

# Connect to SQLite
conn = sqlite3.connect("time_series.db")  # Creates the .db file
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Temperature (
    Time DATETIME NOT NULL,          -- Records time accurate to seconds
    Temperature REAL NOT NULL,       -- Records temperature to two decimal points
    PRIMARY KEY (Time, Temperature)     -- Ensures uniqueness of Time and Temperature
)
""")
conn.commit()

# Insert data from CSV
with open("data_15000.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute("INSERT INTO Temperature (time, temperature) VALUES (?, ?)", (row["time"], row["temperature"]))

conn.commit()
conn.close()

print("SQL database populated with 15,000 unique composite combinations.")
