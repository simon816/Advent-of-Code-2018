import sys
import re

claimre = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

grid = [None] * 1000
for i in range(1000):
    grid[i] = [(None, 0)] * 1000

intact = set()

for line in sys.stdin:
    m = claimre.match(line)
    id, left, top, width, height = map(int, m.groups())
    intact.add(id)
    for x in range(left, left+width):
        for y in range(top, top+height):
            existing, count = grid[y][x]
            if existing is None:
                grid[y][x] = (id, 1)
            else:
                if existing in intact:
                    intact.remove(existing)
                if id in intact:
                    intact.remove(id)
                grid[y][x] = (id, count + 1)

print(intact)

