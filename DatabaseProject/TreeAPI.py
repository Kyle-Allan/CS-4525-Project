from flask import Flask, request, jsonify
from datetime import datetime
from BPlusTree import BPlusTree  # Import the BPlusTree class

app = Flask(__name__)

# Initialize the B+-tree with your specified order
bplustree = BPlusTree(order=5)

@app.route('/insert', methods=['POST'])
def insert():
    try:
        # Get data from the request
        data = request.json
        timestamp = datetime.fromisoformat(data['time'])
        value = data['value']

        # Insert into the B+-tree
        bplustree.insert(timestamp, value)
        return jsonify({'message': 'Data inserted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/query', methods=['GET'])
def query():
    try:
        # Get the start and end times from query parameters
        start_time = datetime.fromisoformat(request.args.get('start'))
        end_time = datetime.fromisoformat(request.args.get('end'))

        # Perform the range query
        results = bplustree.range_query(start_time, end_time)
        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/delete', methods=['POST'])
def delete():
    try:
        # Get the key to delete
        data = request.json
        timestamp = datetime.fromisoformat(data['time'])

        # Delete from the B+-tree
        bplustree.delete(timestamp)
        return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)