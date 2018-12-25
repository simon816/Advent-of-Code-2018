import sys
import re

pat = re.compile('^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$')

bots = []

largest = None
for line in sys.stdin:
    x, y, z, r = map(int, pat.match(line).groups())
    if largest is None or r > largest[1]:
        largest = (len(bots), r)
    bots.append((x, y, z))


i, rad = largest

x, y, z = bots[i]

in_range = 0

for bot in bots:
    bx, by, bz = bot

    dx, dy, dz = abs(x - bx), abs(y - by), abs(z - bz)
    dist = dx + dy + dz
    if dist <= rad:
        in_range += 1

print(in_range)
