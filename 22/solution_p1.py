import sys
from collections import namedtuple

params = dict(map(str.strip, pair.split(':')) for pair in sys.stdin)

depth = int(params['depth'])
tx, ty = map(int, params['target'].split(','))

grid = []

Info = namedtuple('Info', 'geologic erosion type')

def get_levels(x, y):
    if x == tx and y == ty:
        geologic = 0
    elif x == 0 and y == 0:
        geologic = 0
    elif y == 0:
        geologic = x * 16807
    elif x == 0:
        geologic = y * 48271
    else:
        geologic = grid[y][x - 1].erosion * grid[y - 1][x].erosion

    erosion = (geologic + depth) % 20183
    type = erosion % 3#['rocky', 'wet', 'narrow'][erosion % 3]
    return Info(geologic, erosion, type)

for y in range(ty + 1):
    row = []
    grid.append(row)
    for x in range(tx + 1):
        row.append(get_levels(x, y))

risk = 0
for row in grid:
    risk += sum(map(lambda i: i.type, row))

print(risk)
