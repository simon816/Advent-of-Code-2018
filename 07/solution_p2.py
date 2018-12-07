import sys
import re

pat = re.compile('^Step (\w+) must be finished before step (\w+) can begin\.$')

class Node:
    def __init__(self, lbl):
        self.deps = set()
        self.lbl = lbl
        self.dur = 60 + (ord(lbl.upper()) - 64)
        self.remain = self.dur
    def get_lbl(self):
        return self.lbl
    def get_rem(self):
        return self.remain
    def done(self, node):
        if node in self.deps:
            self.deps.remove(node)
    def __repr__(self):
        return 'Node(%s, %d)' % (self.lbl, self.remain)

nodes = {}

for line in sys.stdin:
    m = pat.match(line)
    dep, step = m.groups()
    depnode = nodes.setdefault(dep, Node(dep))
    node = nodes.setdefault(step, Node(step))
    node.deps.add(depnode)

total = 0
N_WORKER = 5
busy = []
while True:
    available = filter(lambda n: not n.deps and n not in busy, nodes.values())
    available = list(sorted(available, key=Node.get_lbl))
    if not nodes:
        break
    for _ in range(N_WORKER):
        if available and len(busy) < N_WORKER:
            busy.append(available.pop(0))
    busy = list(sorted(busy, key=Node.get_rem))
    finishfirst = busy[0]
    while busy and busy[0].remain == finishfirst.remain:
        n = busy.pop(0)
        del nodes[n.lbl]
        for o in nodes.values():
            o.done(n)
    total += finishfirst.remain
    if not nodes:
        break
    for other in busy:
        other.remain -= finishfirst.remain

if busy:
    last = busy[-1]
    total += last.remain

print(total)
