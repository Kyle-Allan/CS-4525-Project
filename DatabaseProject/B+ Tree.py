import math

class Node:
    def __init__(self, order, is_leaf=False):
        self.order = order
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []  # Pointers to child nodes or data values
        self.next = None  # For linking leaf nodes

class BplusTree:
    def __init__(self, order):
        self.root = Node(order, is_leaf=True)

    def insert(self, key, value):
        node = self.root
        if len(node.keys) == node.order - 1:
            # Split root node
            new_root = Node(node.order)
            new_root.is_leaf = False
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            # Insert into the correct position in the leaf
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node.keys.insert(i, key)
            node.children.insert(i, value)
        else:
            # Find the correct child to recurse into
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if len(node.children[i].keys) == node.order - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, index):
        node = parent.children[index]
        mid = len(node.keys) // 2
        new_node = Node(node.order, is_leaf=node.is_leaf)
        parent.keys.insert(index, node.keys[mid])
        parent.children.insert(index + 1, new_node)
        new_node.keys = node.keys[mid + 1:]
        node.keys = node.keys[:mid]
        if node.is_leaf:
            new_node.children = node.children[mid:]
            node.children = node.children[:mid]
            new_node.next = node.next
            node.next = new_node
        else:
            new_node.children = node.children[mid + 1:]
            node.children = node.children[:mid + 1]

    def search(self, key):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node = node.children[i]
        # Search within the leaf node
        for i, item in enumerate(node.keys):
            if key == item:
                return node.children[i]
        return None

    def print_tree(self):
        def print_level(nodes):
            next_level = []
            output = ""
            for node in nodes:
                output += str(node.keys) + " "
                if not node.is_leaf:
                    next_level.extend(node.children)
            print(output)
            if next_level:
                print_level(next_level)
        print_level([self.root])



bplustree = BplusTree(order=4)
bplustree.insert(1, "Value1")
bplustree.insert(2, "Value2")
bplustree.insert(3, "Value3")
bplustree.insert(4, "Value4")
bplustree.insert(5, "Value5")
bplustree.insert(6, "Value6")
bplustree.insert(7, "Value7")

bplustree.print_tree()
result = bplustree.search(5)
print(f"Found: {result}")
