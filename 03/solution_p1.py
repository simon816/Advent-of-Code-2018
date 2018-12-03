import sys
import re

claimre = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

grid = [None] * 1000
for i in range(1000):
    grid[i] = [0] * 1000

collide = set()

for line in sys.stdin:
    m = claimre.match(line)
    id, left, top, width, height = map(int, m.groups())
    for x in range(left, left+width):
        for y in range(top, top+height):
            grid[y][x] += 1
            if grid[y][x] > 1:
                collide.add((x, y))

print(len(collide))

