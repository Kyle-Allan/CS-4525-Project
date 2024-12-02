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



# Insert data from CSV
with open("data_15000.csv", mode="r") as file:
    reader = csv.DictReader(file)
    # Measure insertion time
    start_time = time.time()  # Start the timer
    for row in reader:
        cursor.execute("INSERT INTO Temperature (Time, Temperature) VALUES (?, ?)", (row["time"], row["temperature"]))

conn.commit()  # Commit changes to the database
end_time = time.time()  # Stop the timer

conn.close()

# Print execution time
print(f"SQL database populated with 15,000 unique composite combinations in {end_time - start_time:.2f} seconds.")
