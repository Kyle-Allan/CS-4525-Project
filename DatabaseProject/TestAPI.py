from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS


# List to manage
data_list = [
    {"id": 1, "value": "Apple"},
    {"id": 2, "value": "Banana"},
    {"id": 3, "value": "Cherry"}
]

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route('/list', methods=['GET'])
def get_list():
    """Retrieve the entire list."""
    return jsonify(data_list)

@app.route('/list/search', methods=['GET'])
def search_list():
    """Search the list for a specific value."""
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    result = [item for item in data_list if query.lower() in item["value"].lower()]
    return jsonify(result)

@app.route('/list', methods=['POST'])
def add_to_list():
    """Add a new item to the list."""
    new_item = request.json
    if "id" not in new_item or "value" not in new_item:
        return jsonify({"error": "Both 'id' and 'value' are required"}), 400
    data_list.append(new_item)
    return jsonify({"message": "Item added successfully", "item": new_item}), 201

@app.route('/list/<int:item_id>', methods=['PUT'])
def update_list(item_id):
    """Update an existing item in the list."""
    updated_item = request.json
    for item in data_list:
        if item["id"] == item_id:
            item.update(updated_item)
            return jsonify({"message": "Item updated successfully", "item": item})
    return jsonify({"error": "Item not found"}), 404

@app.route('/list/<int:item_id>', methods=['DELETE'])
def delete_from_list(item_id):
    """Delete an item from the list."""
    global data_list
    data_list = [item for item in data_list if item["id"] != item_id]
    return jsonify({"message": "Item deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
