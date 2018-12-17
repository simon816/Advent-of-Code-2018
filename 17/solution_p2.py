import sys

points = []

maxx = None
maxy = None
minx = None
miny = None

for line in sys.stdin:
    d = dict(map(lambda s: (s[0],
                              list(map(int, s[2:].split('..'))) \
                                    if '.' in s else int(s[2:])), \
                   map(str.strip, line.split(','))))
    xl, yl = d['x'], d['y']
    if type(xl) != list:
        xl = [xl, xl]
    if type(yl) != list:
        yl = [yl, yl]
    for x in range(xl[0], xl[1] + 1):
        for y in range(yl[0], yl[1] + 1):
            points.append((x, y))
            if maxx is None or x > maxx:
                maxx = x
            if maxy is None or y > maxy:
                maxy = y
            if miny is None or y < miny:
                miny = y
            if minx is None or x < minx:
                minx = x

ground = [None] * (maxy + 1)
for y in range(maxy + 1):
    ground[y] = ['.'] * (maxx + 1)

for x, y in points:
    ground[y][x] = '#'

active = []

def drip():
    global active
    change = False
    active_set = set()
    new_active = []
    for x, y in active:
        below = ground[y + 1][x] if y < maxy else None
        left = ground[y][x - 1]
        right = ground[y][x + 1]
        if below is None:
            continue
        if below == '|':
            if (x, y) not in active_set:
                new_active.append((x, y))
                active_set.add((x, y))
            continue
        if below == '.':
            ground[y + 1][x] = '|'
            change = True
            if (x, y + 1) not in active_set:
                new_active.append((x, y + 1))
                active_set.add((x, y + 1))
            ground[y][x] = '.'
            continue
        if left == '.':
            ground[y][x - 1] = '|'
            change = True
            if (x - 1, y) not in active_set:
                new_active.append((x - 1, y))
                active_set.add((x - 1, y))
            ground[y][x] = '.'
            continue
        if right == '.':
            ground[y][x + 1] = '|'
            change = True
            if (x + 1, y) not in active_set:
                new_active.append((x + 1, y))
                active_set.add((x + 1, y))
            ground[y][x] = '.'
            continue
        leftmost = x
        while ground[y][leftmost] != '#' and leftmost != 0:
            leftmost -= 1
        rightmost = x
        while rightmost <= maxx and ground[y][rightmost] != '#':
            rightmost += 1
        can_rest = False
        if leftmost != -1 and rightmost <= maxx:
            for x_test in range(leftmost + 1, rightmost):
                can_rest = ground[y + 1][x_test] in '#~'
                if not can_rest:
                    break
        if can_rest:
            ground[y][x] = '~'
            change = True
        else:
            if (x, y) not in active_set:
                new_active.append((x, y))
                active_set.add((x, y))
    active = new_active
    return change

while True:
    active.append((500, 0))
    ground[0][500] = '|'
    if not drip():
        break
    """
    for row in ground:
        print(''.join(row[minx:]))
    sys.stdout.flush()
    import time
    time.sleep(0.1)
    """

total = 0
for row in ground[miny:]:
    total += row.count('~')

print(total)

