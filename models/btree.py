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

    def delete(self, key):
        if not self.root:
            return

        self._delete_internal(self.root, key)

        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete_internal(self, node, key):
        t = self.t

        # CASE 1 — key ada di node saat ini
        if key in node.keys:
            idx = node.keys.index(key)

            # CASE 1A — jika node adalah leaf → hapus langsung
            if node.leaf:
                node.keys.pop(idx)
                node.values.pop(idx)
                return

            # CASE 1B — node internal → ambil predecessor atau successor
            if len(node.children[idx].keys) >= t:
                pred_node = node.children[idx]
                while not pred_node.leaf:
                    pred_node = pred_node.children[-1]
                pred_key = pred_node.keys[-1]
                pred_val = pred_node.values[-1]

                node.keys[idx] = pred_key
                node.values[idx] = pred_val

                self._delete_internal(node.children[idx], pred_key)

            elif len(node.children[idx + 1].keys) >= t:
                succ_node = node.children[idx + 1]
                while not succ_node.leaf:
                    succ_node = succ_node.children[0]
                succ_key = succ_node.keys[0]
                succ_val = succ_node.values[0]

                node.keys[idx] = succ_key
                node.values[idx] = succ_val

                self._delete_internal(node.children[idx + 1], succ_key)
            else:
                # Merge children
                left = node.children[idx]
                right = node.children[idx + 1]

                left.keys.append(node.keys.pop(idx))
                left.values.append(node.values.pop(idx))

                left.keys.extend(right.keys)
                left.values.extend(right.values)
                left.children.extend(right.children)

                node.children.pop(idx + 1)
                self._delete_internal(left, key)
        else:
            # CASE 2 — key tidak ada di node saat ini
            if node.leaf:
                return  # tidak ada, selesai

            child_index = 0
            while child_index < len(node.keys) and key > node.keys[child_index]:
                child_index += 1

            child = node.children[child_index]

            # Pastikan child punya cukup key
            if len(child.keys) < t:
                self._fill_child(node, child_index)

            self._delete_internal(node.children[child_index], key)

    def _fill_child(self, node, idx):
        t = self.t

        if idx > 0 and len(node.children[idx - 1].keys) >= t:
            left = node.children[idx - 1]
            child = node.children[idx]

            child.keys.insert(0, node.keys[idx - 1])
            child.values.insert(0, node.values[idx - 1])

            if not child.leaf:
                child.children.insert(0, left.children.pop())

            node.keys[idx - 1] = left.keys.pop()
            node.values[idx - 1] = left.values.pop()

        elif idx < len(node.children) - 1 and len(node.children[idx + 1].keys) >= t:
            right = node.children[idx + 1]
            child = node.children[idx]

            child.keys.append(node.keys[idx])
            child.values.append(node.values[idx])

            if not child.leaf:
                child.children.append(right.children.pop(0))

            node.keys[idx] = right.keys.pop(0)
            node.values[idx] = right.values.pop(0)

        else:
            if idx < len(node.children) - 1:
                child = node.children[idx]
                right = node.children[idx + 1]

                child.keys.append(node.keys.pop(idx))
                child.values.append(node.values.pop(idx))

                child.keys.extend(right.keys)
                child.values.extend(right.values)
                child.children.extend(right.children)

                node.children.pop(idx + 1)
            else:
                child = node.children[idx - 1]
                right = node.children[idx]

                child.keys.append(node.keys.pop(idx - 1))
                child.values.append(node.values.pop(idx - 1))

                child.keys.extend(right.keys)
                child.values.extend(right.values)
                child.children.extend(right.children)

                node.children.pop(idx)
