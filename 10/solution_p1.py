import sys
import re
import io

num = r'<\s*(-?\d+),\s+(-?\d+)>'
pattern = re.compile('^position=%s velocity=%s$' % (num, num))

points = []
velocities = []

for line in sys.stdin:
    m = pattern.match(line)
    px, py, vx, vy = map(int, m.groups())
    points.append((px, py))
    velocities.append((vx, vy))

def plot():
    lines = {}
    minx, maxx = None, None
    for x, y in points:
        if y > 500 or y < -500:
            return False
        lines.setdefault(y, set())
        lines[y].add(x)
        if minx is None or x < minx:
            minx = x
        if maxx is None or x > maxx:
            maxx = x
    nexty = None
    f = io.StringIO()
    for y in sorted(lines.keys()):
        tmp = y
        while nexty is not None and tmp > nexty:
            print('.' * (maxx - minx), file=f)
            tmp -= 1
        line = lines[y]
        s = ''
        maxrun = 0
        run = 0
        expect = None
        for x in range(minx, maxx + 1):
            if x == expect:
                run += 1
            else:
                if run > maxrun: maxrun = run
                run = 0
            s += '#' if x in line else '.'
            expect = x + 1
        if run > maxrun: maxrun = run
        if maxrun < 10:
            return False
        print(s, file=f)
        nexty = y + 1
    print(f.getvalue())
    return True

def tick():
    for i in range(len(points)):
        x, y = points[i]
        points[i] = (x + velocities[i][0], y + velocities[i][1])

plot()

import time

t = 0
while True:
    tick()
    t += 1
    print("t = %d" % t)
    if plot():
        time.sleep(3)
