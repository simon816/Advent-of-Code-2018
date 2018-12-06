import sys

points = []
for line in sys.stdin:
    x, y = map(int, map(str.strip, line.split(",")))
    points.append((x, y))

max_x = max(map(lambda p: p[0], points))
max_y = max(map(lambda p: p[1], points))

grid = [None] * (max_y + 1)
for y in range(max_y + 1):
    grid[y] = [None] * (max_x + 1)

def dist_sum(x, y):
    tot = 0
    for n, (x1, y1) in enumerate(points):
        tot += abs(x - x1) + abs(y - y1)
    return tot < 10000

region = 0
for y, row in enumerate(grid):
    for col in range(len(row)):
        if dist_sum(col, y):
            region += 1

print(region)
