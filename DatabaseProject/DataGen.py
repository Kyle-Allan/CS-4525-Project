import csv
from datetime import datetime, timedelta
import random

# Generate unique time-value combinations
def generate_unique_combinations(start_time, num_entries, interval_seconds, value_range):
    """
    Generate a list of unique time-value combinations where the combination is unique.
    """
    combinations = set()  # Use a set to ensure uniqueness

    # Generate timestamps incrementally
    timestamps = [start_time + timedelta(seconds=i * interval_seconds) for i in range(num_entries)]

    # Generate unique time-value pairs
    while len(combinations) < num_entries:
        for timestamp in timestamps:
            value = round(random.uniform(*value_range), 2)  # Generate a random float
            if (timestamp.isoformat(), value) not in combinations:
                combinations.add((timestamp.isoformat(), value))
            if len(combinations) == num_entries:
                break

    return list(combinations)

# Initialize parameters
start_time = datetime(2024, 1, 1, 0, 0, 0)  # Start timestamp
num_entries = 150000  # Number of rows
interval_seconds = 1  # Spacing between timestamps
value_range = (-50, 50)  # Range for random float values (e.g., temperature)

# Generate unique time-value combinations
entries = generate_unique_combinations(start_time, num_entries, interval_seconds, value_range)

# Save entries to a CSV file
output_file = "data_150000.csv"

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["time", "value"])  # Write header
    writer.writerows(entries)          # Write rows

print(f"{num_entries} unique composite combinations have been written to {output_file}.")
