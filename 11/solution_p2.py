import sys

def power_level(x, y, serial):
    id = x + 10
    power = id * y
    power += serial
    power *= id
    hundred = (power // 100) % 10
    return hundred - 5


def make_grid():
    grid = [None] * 300
    serial = 7511#int(sys.stdin.read().strip())
    for y in range(300):
        grid[y] = [power_level(x + 1, y + 1, serial) for x in range(300)]
    return grid

grid = make_grid()

def get_level(center_x, center_y, size):
    total = 0
    half = size // 2
    rem = size - half
    low_y = center_y - half
    high_y = center_y + rem
    low_x = center_x - half
    high_x = center_x + rem
    if low_y < 0 or high_y > 300 or low_x < 0 or high_x > 300:
        return None, low_x, low_y
    for line in grid[low_y : high_y]:
        total += sum(line[low_x : high_x])
    return total, low_x, low_y

def get_max(size):
    print(size)
    max_val = None
    max_coord = None
    for cx in range(300):
        for cy in range(300):
            level, lx, ly = get_level(cx, cy, size)
            if level is None:
                continue
            if max_val is None or level > max_val:
                max_val = level
                max_coord = (lx + 1, ly + 1)
    return max_val, max_coord, size

from multiprocessing import Pool

def run():
    pool = Pool()
    mapres = pool.map_async(get_max, range(1, 301))
    val = mapres.get()
    print(max(val, key = lambda r: r[0]))

if __name__ == '__main__':
    run()
