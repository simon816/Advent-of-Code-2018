import sys

def power_level(x, y, serial):
    id = x + 10
    power = id * y
    power += serial
    power *= id
    hundred = (power // 100) % 10
    return hundred - 5


grid = [None] * 300

serial = int(sys.stdin.read().strip())

for y in range(300):
    grid[y] = [power_level(x + 1, y + 1, serial) for x in range(300)]

def get_3x3_level(center_x, center_y):
    total = 0
    for line in grid[center_y - 1 : center_y + 2]:
        total += sum(line[center_x - 1 : center_x + 2])
    return total

max_val = None
max_coord = None

for cx in range(1, 299):
    for cy in range(1, 299):
        level = get_3x3_level(cx, cy)
        if max_val is None or level > max_val:
            max_val = level
            max_coord = (cx, cy)

print(max_coord, max_val)
