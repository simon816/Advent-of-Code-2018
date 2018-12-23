import sys
from collections import namedtuple

params = dict(map(str.strip, pair.split(':')) for pair in sys.stdin)

depth = int(params['depth'])
tx, ty = map(int, params['target'].split(','))

#depth=510
#tx=ty=10

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

    @staticmethod
    def create(dat):
        if 'node' in dat.meta:
            return dat.meta['node']
        obj = Node(dat)
        dat.meta['node'] = obj
        return obj
    
    def __init__(self, dat):
        self.d = dat
        self.cost = None
        self.perm = False
        self.adj = None
        self.t_to_parent = {}

    def set_cost(self, cost, tool, parent):
        assert not self.perm
        if self.cost is None or cost < self.cost:
            self.cost = cost
            self.t_to_parent = {tool: parent}
        elif self.cost == cost:
            # It is equally optimal to reach here with a different tool,
            # so have the flexiblity of choosing either tool
            if tool not in self.t_to_parent:
               self.t_to_parent[tool] = parent

    def tools(self):
        return ''.join(self.t_to_parent.keys())

    def switch_to(self, other):
        can_use = tool_use[self.d.type]
        if other.is_target():
            # If we're not using a torch and cannot switch to torch, path
            # inaccessable
            use_t = 't' in can_use
            if 't' not in self.t_to_parent and not use_t:
                return False, False
            if use_t:
                return ['t'], False
            return ['t'], True
        can_use_other = tool_use[other.d.type]
        propagated = []
        for our_tool in self.t_to_parent.keys():
            if our_tool in can_use_other:
                propagated.append(our_tool)
        if propagated:
            return propagated, False
        our_only = list(self.t_to_parent.keys())
        assert len(our_only) == 1
        return [[c for c in can_use if c != our_only[0]][0]], True
        

    def is_target(self):
        return self.d.x == tx and self.d.y == ty

    def weight(self):
        return self.cost

    def mk_perm(self):
        assert not self.perm
        self.perm = True
        if self.cost > max_cost:
            self.adj = []

    def adjacent(self):
        assert self.perm
        if self.adj is None:
            self.adj = []
            for adj in map(Node.create, get_adjacent(self.d)):
                if adj.perm:
                    continue
                next_tools, switch = self.switch_to(adj)
                if next_tools == False:
                    continue
                extra = 7 if switch else 0
                self.adj.append(adj)
                for tool in next_tools:
                    adj.set_cost(self.cost + 1 + extra, tool, self)
        return self.adj

def dump():
    for row in grid:
        l = ''
        for cell in row:
            if 'node' in cell.meta:
                w = cell.meta['node'].weight()
                if w is None:
                    s = 'NNNN'
                else:
                    s = '%02d%2s' % (w, cell.meta['node'].tools())
            else:
                if cell.x == tx and cell.y == ty:
                    s = 'TTTT'
                else:
                    s = '????'
            l += s + '|'
        print(l)
    print('\n' * (30 - len(grid)))

root = Node.create(grid[0][0])
root.set_cost(0, 't', None)

node = root
adj_list = set()
while True:
    node.mk_perm()
    #dump()
    for adj in node.adjacent():
        adj_list.add(adj)
    node = min(adj_list, key=Node.weight)
    adj_list.remove(node)
    print("chose", node.weight(), node.tools(), node.d, len(adj_list))
    if node.is_target():
        print(node.weight())
        break
