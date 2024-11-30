from flask import Flask, request, jsonify
from datetime import datetime
import math

# Node creation
class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.nextKey = None
        self.parent = None
        self.check_leaf = False

    def insert_at_leaf(self, value, key):
        if self.values:
            for i in range(len(self.values)):
                if value == self.values[i]:
                    self.keys[i].append(key)
                    break
                elif value < self.values[i]:
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif i + 1 == len(self.values):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]


class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.check_leaf = True

    def insert(self, value, key):
        old_node = self.search(value)
        old_node.insert_at_leaf(value, key)

        if len(old_node.values) == old_node.order:
            node1 = Node(old_node.order)
            node1.check_leaf = True
            node1.parent = old_node.parent
            mid = int(math.ceil(old_node.order / 2)) - 1
            node1.values = old_node.values[mid + 1:]
            node1.keys = old_node.keys[mid + 1:]
            node1.nextKey = old_node.nextKey
            old_node.values = old_node.values[:mid + 1]
            old_node.keys = old_node.keys[:mid + 1]
            old_node.nextKey = node1
            self.insert_in_parent(old_node, node1.values[0], node1)

    def search(self, value):
        current_node = self.root
        while not current_node.check_leaf:
            for i in range(len(current_node.values)):
                if value == current_node.values[i]:
                    current_node = current_node.keys[i + 1]
                    break
                elif value < current_node.values[i]:
                    current_node = current_node.keys[i]
                    break
                elif i + 1 == len(current_node.values):
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

    def retrieve_between_dates(self, start_date, end_date):
        """
        Retrieve all entries between two datetime values (inclusive).
        """
        result = []
        current_node = self.root

        # Traverse to the leftmost leaf node
        while not current_node.check_leaf:
            current_node = current_node.keys[0]  # Go to the leftmost child

        # Traverse leaf nodes and collect entries within the range
        while current_node:
            for i, value in enumerate(current_node.values):
                if start_date <= value <= end_date:
                    result.append((value, current_node.keys[i]))
            current_node = current_node.nextKey  # Move to the next linked leaf node

        return result

    def insert_in_parent(self, n, value, ndash):
        if self.root == n:
            rootNode = Node(n.order)
            rootNode.values = [value]
            rootNode.keys = [n, ndash]
            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            return

        parentNode = n.parent
        for i in range(len(parentNode.keys)):
            if parentNode.keys[i] == n:
                parentNode.values = parentNode.values[:i] + [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i + 1] + [ndash] + parentNode.keys[i + 1:]
                if len(parentNode.keys) > parentNode.order:
                    parentdash = Node(parentNode.order)
                    parentdash.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2)) - 1
                    parentdash.values = parentNode.values[mid + 1:]
                    parentdash.keys = parentNode.keys[mid + 1:]
                    value_ = parentNode.values[mid]
                    parentNode.values = parentNode.values[:mid]
                    parentNode.keys = parentNode.keys[:mid + 1]
                    for j in parentNode.keys:
                        j.parent = parentNode
                    for j in parentdash.keys:
                        j.parent = parentdash
                    self.insert_in_parent(parentNode, value_, parentdash)
                return


# Initialize Flask app and B+ tree
app = Flask(__name__)
bplustree = BplusTree(order=4)  # Initialize B+ tree with order 4


@app.route('/insert', methods=['POST'])
def insert():
    """
    Insert a key-value pair into the B+ tree.
    """
    data = request.get_json()
    try:
        value = data['value']
        key = datetime.strptime(data['key'], "%Y-%m-%d %H:%M:%S")
        bplustree.insert(key, value)
        return jsonify({"message": "Inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/search', methods=['GET'])
def search():
    """
    Search for a specific key in the B+ tree.
    """
    key_str = request.args.get('key')
    try:
        key = datetime.strptime(key_str, "%Y-%m-%d %H:%M:%S")
        node = bplustree.search(key)
        for i, value in enumerate(node.values):
            if value == key:
                return jsonify({"key": key_str, "values": node.keys[i]}), 200
        return jsonify({"message": "Key not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/retrieve_between', methods=['GET'])
def retrieve_between():
    """
    Retrieve all entries between two datetime values.
    """
    start_str = request.args.get('start')
    end_str = request.args.get('end')
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
        result = bplustree.retrieve_between_dates(start_date, end_date)
        formatted_result = [{"value": value, "key": [key.strftime("%Y-%m-%d %H:%M:%S") for key in keys]} for value, keys in result]
        return jsonify(formatted_result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
