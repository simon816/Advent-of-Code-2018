import sys

numbers = list(map(int, sys.stdin.read().strip().split(' ')))

class Node:
    def __init__(self):
        self.children = []
        self.meta = []
    def get_all(self):
        all = [self]
        for c in self.children:
            all.extend(c.get_all())
        return all
    def get_val(self):
        if not self.children:
            return sum(self.meta)
        val = 0
        for i in self.meta:
            i -= 1
            if i < len(self.children) and i >= 0:
                val += self.children[i].get_val()
        return val

def read_node(data):
    n_child, n_meta, *xs = data
    node = Node()
    for n in range(n_child):
        child, xs = read_node(xs)
        node.children.append(child)
    meta, xs = xs[:n_meta], xs[n_meta:]
    node.meta = meta
    return node, xs

root,_ = read_node(numbers)

print(root.get_val())
