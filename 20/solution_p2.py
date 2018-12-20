import sys

regex = sys.stdin.read().strip()

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

print(sum(1 for v in pos_to_distance.values() if v >= 1000))
