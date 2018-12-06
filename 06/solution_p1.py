import sys

points = []
for line in sys.stdin:
    x, y = map(int, map(str.strip, line.split(",")))
    points.append((x, y))

# All of this is just eww

max_x = max(map(lambda p: p[0], points))
max_y = max(map(lambda p: p[1], points))

grid = [None] * (max_y + 1)
for y in range(max_y + 1):
    grid[y] = [None] * (max_x + 1)

def closest(x, y):
    all_i = [0]
    cx, cy = points[0]
    best = abs(x - cx) + abs(y - cy)
    maybe_collide = False
    for n, (x1, y1) in enumerate(points):
        if n == 0:
            continue
        d = abs(x - x1) + abs(y - y1)
        if d < best:
            maybe_collide = False
            best = d
            all_i = [n]
        elif d == best:
            all_i.append(n)
    return all_i

for y, row in enumerate(grid):
    for col in range(len(row)):
        row[col] = closest(col, y)

inf = set()

toprow = grid[0]
for a in toprow:
    if len(a) == 1:
        inf.add(a[0])
bottomrow = grid[-1]
for a in bottomrow:
    if len(a) == 1:
        inf.add(a[0])
for y in range(max_y):
    left, right = grid[y][0], grid[y][-1]
    if len(left) == 1:
        inf.add(left[0])
    if len(right) == 1:
        inf.add(right[0])

def count(n):
    c = 0
    for row in grid:
        for col in row:
            if len(col) == 1 and col[0] == n:
                c += 1
    return c

counts = []
for i in range(len(points)):
    if i in inf:
        continue
    counts.append(count(i))

print(max(counts))
