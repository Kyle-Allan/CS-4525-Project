import csv
from datetime import datetime, timedelta
import random

# Generate 15,000 unique time-value combinations
def generate_unique_combinations(start_time, num_entries, interval_seconds, value_range):
    """
    Generate a list of unique time-value combinations where the combination is unique.
    """
    combinations = set()  # Use a set to ensure uniqueness
    timestamps = [start_time + timedelta(seconds=i * interval_seconds) for i in range(num_entries)]

    while len(combinations) < num_entries:
        for timestamp in timestamps:
            value = random.randint(*value_range)  # Generate a random value
            combinations.add((timestamp.isoformat(), value))
            if len(combinations) == num_entries:
                break

    return list(combinations)

# Initialize parameters
start_time = datetime(2024, 1, 1, 0, 0, 0)
num_entries = 15000
interval_seconds = 1  # Ensure timestamps are spaced apart
value_range = (1, 100)  # Define the range for random values

# Generate unique time-value combinations
entries = generate_unique_combinations(start_time, num_entries, interval_seconds, value_range)

# Save entries to a CSV file
output_file = "data_15000.csv"

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["time", "value"])  # Write header
    writer.writerows(entries)          # Write rows

print(f"15,000 unique composite combinations have been written to {output_file}.")
