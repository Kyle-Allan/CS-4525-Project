import math
from datetime import datetime

# Node creation
class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.nextKey = None
        self.parent = None
        self.check_leaf = False

    # Insert at the leaf
    def insert_at_leaf(self, leaf, value, key):
        if (self.values):
            temp1 = self.values
            for i in range(len(temp1)):
                if (value == temp1[i]):
                    self.keys[i].append(key)
                    break
                elif (value < temp1[i]):
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    break
                elif (i + 1 == len(temp1)):
                    self.values.append(value)
                    self.keys.append([key])
                    break
        else:
            self.values = [value]
            self.keys = [[key]]


# B plus tree
class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.check_leaf = True

    # Insert operation
    def insert(self, value, key):
        value = str(value)
        old_node = self.search(value)
        old_node.insert_at_leaf(old_node, value, key)

        if (len(old_node.values) == old_node.order):
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

    # Search operation for different operations
    def search(self, value):
        current_node = self.root
        while(current_node.check_leaf == False):
            temp2 = current_node.values
            for i in range(len(temp2)):
                if (value == temp2[i]):
                    current_node = current_node.keys[i + 1]
                    break
                elif (value < temp2[i]):
                    current_node = current_node.keys[i]
                    break
                elif (i + 1 == len(current_node.values)):
                    current_node = current_node.keys[i + 1]
                    break
        return current_node

    # Find the node
    def find(self, value, key):
        l = self.search(value)
        for i, item in enumerate(l.values):
            if item == value:
                if key in l.keys[i]:
                    return True
                else:
                    return False
        return False

    # Inserting at the parent
    def insert_in_parent(self, n, value, ndash):
        if (self.root == n):
            rootNode = Node(n.order)
            rootNode.values = [value]
            rootNode.keys = [n, ndash]
            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            return

        parentNode = n.parent
        temp3 = parentNode.keys
        for i in range(len(temp3)):
            if (temp3[i] == n):
                parentNode.values = parentNode.values[:i] + \
                    [value] + parentNode.values[i:]
                parentNode.keys = parentNode.keys[:i +
                                                  1] + [ndash] + parentNode.keys[i + 1:]
                if (len(parentNode.keys) > parentNode.order):
                    parentdash = Node(parentNode.order)
                    parentdash.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2)) - 1
                    parentdash.values = parentNode.values[mid + 1:]
                    parentdash.keys = parentNode.keys[mid + 1:]
                    value_ = parentNode.values[mid]
                    if (mid == 0):
                        parentNode.values = parentNode.values[:mid + 1]
                    else:
                        parentNode.values = parentNode.values[:mid]
                    parentNode.keys = parentNode.keys[:mid + 1]
                    for j in parentNode.keys:
                        j.parent = parentNode
                    for j in parentdash.keys:
                        j.parent = parentdash
                    self.insert_in_parent(parentNode, value_, parentdash)

# Print the tree
def printTree(tree):
    lst = [tree.root]
    level = [0]
    leaf = None
    flag = 0
    lev_leaf = 0

    node1 = Node(str(level[0]) + str(tree.root.values))

    while (len(lst) != 0):
        x = lst.pop(0)
        lev = level.pop(0)
        if (x.check_leaf == False):
            for i, item in enumerate(x.keys):
                print(item.values)
        else:
            for i, item in enumerate(x.keys):
                print(item.values)
            if (flag == 0):
                lev_leaf = lev
                leaf = x
                flag = 1


def retrieve_between_dates(tree, start_date, end_date):
    """
    Retrieve all entries between two datetime values (inclusive).

    :param tree: The B+ Tree instance.
    :param start_date: The start datetime (inclusive).
    :param end_date: The end datetime (inclusive).
    :return: A list of (value, key) tuples that fall within the range.
    """
    if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
        raise ValueError("Both start_date and end_date must be datetime objects.")

    result = []
    current_node = tree.root

    # Traverse to the leftmost leaf node
    while not current_node.check_leaf:
        current_node = current_node.keys[0]  # Go to the leftmost child

    # Traverse leaf nodes and collect entries within the range
    while current_node:
        for i, value in enumerate(current_node.values):
            for key in current_node.keys[i]:
                if start_date <= key <= end_date:
                    result.append((value, key))
        current_node = current_node.nextKey  # Move to the next linked leaf node

    return result


record_len = 3
bplustree = BplusTree(record_len)
bplustree.insert('1', datetime(2023, 12, 1, 12, 0, 0))
bplustree.insert('2', datetime(2023, 12, 2, 12, 0, 0))
bplustree.insert('3', datetime(2023, 12, 3, 12, 0, 0))
bplustree.insert('4', datetime(2023, 12, 4, 12, 0, 0))
bplustree.insert('5', datetime(2023, 12, 5, 12, 0, 0))


if(bplustree.find('3', datetime(2023, 12, 3, 12, 0, 0))):
    print("Found")
else:
    print("Not found")


# Define the range
start = datetime(2023, 12, 2, 12, 0, 0)
end = datetime(2023, 12, 4, 12, 0, 0)

# Retrieve entries between the range
entries = retrieve_between_dates(bplustree, start, end)

# Print the results
print("Entries between dates:")
for value, key in entries:
    print(f"Value: {value}, Key: {key}")