from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "time_series.db"

# Define a route for the root URL
@app.route("/")
def home():
    return "Hello, Flask!"

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables dict-like row access
    return conn

# Route to fetch all data
@app.route('/temperature', methods=['GET'])
def get_all_temperatures():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Temperature")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Route to fetch data by exact timestamp
@app.route('/temperature/<timestamp>', methods=['GET'])
def get_temperature_by_timestamp(timestamp):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Temperature WHERE Time = ?", (timestamp,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    else:
        return jsonify({"error": "Data not found"}), 404

# Route for range query
@app.route('/temperature/range', methods=['GET'])
def get_temperatures_in_range():
    start_time = request.args.get('start')
    end_time = request.args.get('end')
    if not start_time or not end_time:
        return jsonify({"error": "Start and end times are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM Temperature
    WHERE Time BETWEEN ? AND ?
    """, (start_time, end_time))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
