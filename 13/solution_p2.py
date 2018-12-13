import sys

grid = []

carts = []

track_lookup = {
    '>': '-',
    '<': '-',
    '^': '|',
    'v': '|'
}

left_lookup = {
    '>': '^',
    '<': 'v',
    '^': '<',
    'v': '>'
}

right_lookup = {
    '>': 'v',
    '<': '^',
    '^': '>',
    'v': '<'
}

class Cart:
    def __init__(self, x, y, piece):
        self.x = x
        self.y = y
        self.track = track_lookup[piece]
        self.dir = piece
        self.state = 0

    @property
    def loc(self):
        return self.x, self.y

    def intersection_turn(self):
        if self.state == 0:
            # left
            self.state = 1
            self.dir = left_lookup[self.dir]
        elif self.state == 1:
            # straight
            self.state = 2
        elif self.state == 2:
            # right
            self.state = 0
            self.dir = right_lookup[self.dir]
        else:
            assert False
        return self.dir

y = 0
for line in sys.stdin:
    line = line[:-1]
    grid.append(list(line))
    for x in range(len(line)):
        piece = line[x]
        if piece in '<>^v':
            track = track_lookup[piece]
            carts.append(Cart(x, y, piece))
    y += 1

fslash_turn = {
    '>': '^',
    '<': 'v',
    '^': '>',
    'v': '<',
}
bslash_turn = {
    '>': 'v',
    '<': '^',
    '^': '<',
    'v': '>',
}

while len(carts) > 1:
    remove = set()
    for cart in carts:
        if cart.loc in remove:
            continue
        x, y = cart.loc
        curr = cart.dir
        if curr == '<':
            nx, ny = x - 1, y
        elif curr == '>':
            nx, ny = x + 1, y
        elif curr == '^':
            nx, ny = x, y - 1
        elif curr == 'v':
            nx, ny = x, y + 1
        next = grid[ny][nx]
        if next in '<>^v':
            remove.add(cart.loc)
            remove.add((nx, ny))
            continue
        grid[y][x] = cart.track
        cart.x = nx
        cart.y = ny
        cart.track = next
        if next == '+':
            grid[ny][nx] = cart.intersection_turn()
        elif next == '/':
            grid[ny][nx] = cart.dir = fslash_turn[curr]
        elif next == '\\':
            grid[ny][nx] = cart.dir = bslash_turn[curr]
        else:
            grid[ny][nx] = cart.dir
    new_carts = []
    for cart in carts:
        if cart.loc in remove:
            grid[cart.y][cart.x] = cart.track
        else:
            new_carts.append(cart)
    carts = sorted(new_carts, key=lambda c: c.loc)

print(carts[0].loc)
