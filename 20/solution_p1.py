import sys

regex = sys.stdin.read().strip()

# This didn't work
"""
import sre_parse
from sre_constants import *

p = sre_parse.parse(regex)

root_list = p.data

assert root_list[0] == (AT, AT_BEGINNING)
assert root_list[-1] == (AT, AT_END)

N, E, S, W = map(ord, 'NESW')

def make_paths(branch):
    path = []
    for op, av in branch:
        if op is LITERAL:
            path.append(av)
        elif op is SUBPATTERN:
            pattern = av[-1]
            path.extend(make_paths(pattern.data))
        elif op is BRANCH:
            _, branches = av
            for br in branches:
                if len(br.data) == 0:
                    pass#continue
            path.extend(max(map(lambda b: make_paths(b.data), branches),
                            key=len))
        elif op is IN:
            path.extend(max(map(lambda c: make_paths([c]), av),
                            key=len))
        else:
            assert False, 'Bad op ' + str((op, av))
    return path

def traverse(branch):
    node = []
    for op, av in branch:
        if op is LITERAL:
            node.append(av)
        elif op is SUBPATTERN:
            pattern = av[-1]
            node.append(traverse(pattern.data))
        elif op is BRANCH:
            _, branches = av
            nodes = [traverse(br.data) for br in branches]
            node.append(nodes)
        elif op is IN:
            nodes = [traverse([choice]) for choice in av]
            node.append(nodes)
        else:
            assert False
    return node

#longest = make_paths(root_list[1:-1])

root = traverse(root_list[1:-1])

def route(depth, node, x, y):
    for path in node:
        if path == N: y -= 1
        elif path == E: x += 1
        elif path == S: y += 1
        elif path == W: x -= 1
        elif type(path) == list:
            route(depth + 1, path, x, y)
        else:
            assert False
route(0, root, 0, 0)
"""

x, y = 0, 0
pos_to_distance = {}
stack = []
d = 0
for c in regex[1:-1]:
    if c in 'NESW':
        if c == 'N':y -= 1
        elif c == 'E': x += 1
        elif c == 'S': y += 1
        elif c == 'W': x -= 1
        d += 1
        if (x, y) in pos_to_distance:
            pos_to_distance[(x, y)] = min(pos_to_distance[(x, y)], d)
        else:
            pos_to_distance[(x, y)] = d
    elif c == '(':
        stack.append((x, y, d))
    elif c == '|':
        x, y, d = stack[-1]
    elif c == ')':
        x, y, d = stack.pop()

print(max(pos_to_distance.values()))
