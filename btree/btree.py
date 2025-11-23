from .node import BTreeNode

class BTree:
    def __init__(self, t):
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    def search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        if node.leaf:
            return None
        return self.search(node.children[i], key)

    def split_child(self, parent, index):
        t = self.t
        node = parent.children[index]
        new_node = BTreeNode(t, leaf=node.leaf)
        parent.keys.insert(index, node.keys[t - 1])
        parent.values.insert(index, node.values[t - 1])
        parent.children.insert(index + 1, new_node)
        new_node.keys = node.keys[t:]
        new_node.values = node.values[t:]
        node.keys = node.keys[:t - 1]
        node.values = node.values[:t - 1]
        if not node.leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]

    def insert(self, key, value):
        root = self.root
        if root.is_full():
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(new_root, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.leaf:
            i = len(node.keys) - 1
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if node.children[i].is_full():
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def traverse(self, node=None):
        if node is None:
            node = self.root
        result = []
        for i in range(len(node.keys)):
            if not node.leaf:
                result.extend(self.traverse(node.children[i]))
            result.append((node.keys[i], node.values[i]))
        if not node.leaf:
            result.extend(self.traverse(node.children[-1]))
        return result
