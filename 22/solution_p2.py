import sys
from collections import namedtuple
from queue import PriorityQueue

params = dict(map(str.strip, pair.split(':')) for pair in sys.stdin)

depth = int(params['depth'])
tx, ty = map(int, params['target'].split(','))

grid = []

Info = namedtuple('Info', 'x y geologic erosion type meta')

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
    return Info(x, y, geologic, erosion, type, {})

def gen_up_to(x, y):
    ry = 0
    for row in grid:
        while len(row) <= x:
            row.append(get_levels(len(row), ry))
        ry += 1
    for y in range(len(grid), y + 1):
        row = []
        grid.append(row)
        for rx in range(x + 1):
            row.append(get_levels(rx, y))

gen_up_to(tx, ty)

maxx = tx
def get_adjacent(loc):
    x, y = loc.x, loc.y
    adj = []
    if y > 0:
        adj.append(grid[y - 1][x])
    if x > 0:
        adj.append(grid[y][x - 1])
    if y >= len(grid) - 2 or x >= len(grid[y]) - 1:
        global maxx
        maxx += 1
        gen_up_to(maxx, y + 1)
    adj.append(grid[y + 1][x])
    adj.append(grid[y][x + 1])
    return adj

tool_use = ['ct', 'cn', 'tn']

# upper bound for the amount of exploration to do
max_cost = (tx + ty) * 7

class Node:

    def __init__(self, dat, cost, tool):
        self.d = dat
        self.cost = cost
        self.tool = tool

    def __lt__(self,o): return self.cost < o.cost
    def __le__(self,o): return self.cost <= o.cost 
    def __gt__(self,o): return self.cost > o.cost
    def __ge__(self,o): return self.cost >= o.cost
    def __eq__(self,o): return self.cost == o.cost
    def __ne__(self,o): return self.cost != o.cost

    def can_use_zero_cost(self, od):
        can_use_other = tool_use[od.type]
        if od.x == tx and od.y == ty:
            return self.tool == 't'
        return self.tool in can_use_other

    def alternative_tool(self):
        can_use = tool_use[self.d.type]
        return [c for c in can_use if c != self.tool][0]

    def is_target(self):
        return self.d.x == tx and self.d.y == ty

    def weight(self):
        return self.cost

    def adjacent(self):
        out = []
        alt = self.alternative_tool()
        for adj in get_adjacent(self.d):
            zero = self.can_use_zero_cost(adj)
            if zero:
                out.append(Node(adj, self.cost + 1, self.tool))
            out.append(Node(adj, self.cost + 8, alt))
        return out

    @property
    def ident(self):
        return self.d.x, self.d.y, self.tool

def dump():
    for row in grid:
        l = ''
        for cell in row:
            if 'node' in cell.meta:
                w = cell.meta['node'].weight()
                if w is None:
                    s = 'NNNNN'
                else:
                    tools =  cell.meta['node'].tools()
                    s = '%03d%2s' % (w, tools.upper() if cell.meta['node'].is_target() else tools)
            else:
                if cell.x == tx and cell.y == ty:
                    s = 'TTTTT'
                else:
                    s = '?????'
            l += str(cell.type) + ':' + s + '|'
        print(l)
    print('\n' * (30 - len(grid)))

root = Node(grid[0][0], 0, 't')

queue = PriorityQueue()
queue.put(root)

prev_best = {}

while True:
    node = queue.get()
    print("chose", node.weight(), node.tool, node.d, queue.qsize())
    if node.is_target():
        print(node.weight() + 1) # off by one, need to investigate
        break
    if node.ident in prev_best and prev_best[node.ident] <= node.cost:
        continue
    prev_best[node.ident] = node.cost
    for adj in node.adjacent():
        queue.put(adj)

