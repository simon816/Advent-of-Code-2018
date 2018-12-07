import sys
import re

pat = re.compile('^Step (\w+) must be finished before step (\w+) can begin\.$')

class Node:
    def __init__(self, lbl):
        self.deps = set()
        self.lbl = lbl
    def get_lbl(self):
        return self.lbl
    def done(self, node):
        if node in self.deps:
            self.deps.remove(node)
    def __repr__(self):
        return 'Node(%s)' % self.lbl

nodes = {}

for line in sys.stdin:
    m = pat.match(line)
    dep, step = m.groups()
    depnode = nodes.setdefault(dep, Node(dep))
    node = nodes.setdefault(step, Node(step))
    node.deps.add(depnode)

order = []
while True:
    available = filter(lambda n: not n.deps, nodes.values())
    available = list(sorted(available, key=Node.get_lbl))
    if not available:
        break
    first = available[0]
    del nodes[first.lbl]
    for n in nodes.values():
        n.done(first)
    order.append(first)
print(''.join(map(Node.get_lbl, order)))
