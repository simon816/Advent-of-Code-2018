import sys
import re

pat = re.compile('^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$')

bots = []

for line in sys.stdin:
    x, y, z, r = map(int, pat.match(line).groups())
    bots.append((x, y, z, r))


# Credit to https://old.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/ecdqzdg/
# It's stupid but it works
# still want to find proper solution though

dist_list = []

for (x, y, z, r) in bots:
    dist = sum(map(abs, (x, y, z)))
    dist_list.append(('begin', max(0, dist - r)))
    dist_list.append(('end', dist + r))


count = 0
best = (0, 0)
for type, d in sorted(dist_list, key=lambda t: t[1]):
    if type == 'begin':
        count += 1
    elif type == 'end':
        count -= 1

    if count > best[0]:
        best = (count, d)

print(best)
