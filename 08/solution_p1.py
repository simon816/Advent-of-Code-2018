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

t = 0
nodes = root.get_all()
for node in nodes:
    t += sum(node.meta)
print(t)
