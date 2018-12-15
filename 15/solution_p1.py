import sys
from collections import namedtuple

def reading_order(obj):
    return (obj.y, obj.x)

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '%s(%d,%d)' % (type(self).__name__, self.x, self.y)

    def __str__(self):
        return self.marker

class Wall(Object):
    marker = '#'

class Empty(Object):
    marker = '.'

class Unit(Object):

    def __init__(self, world, x, y):
        super().__init__(x, y)
        self.world = world
        self.attack_power = 3
        self.hp = 200

    def is_dead(self):
        return self.hp <= 0

    def attack(self, other):
        other.hp -= self.attack_power
        if other.is_dead():
            self.world.dead_unit(other)

    def tick(self, attack_only=False):
        if self.is_dead():
            return True
        targets = self.world.targets_for(self)
        if not targets:
            return False
        candidates = []
        attack = []
        for target in targets:
            adj = self.world.get_adjacent(target)
            in_range = self in adj
            if in_range:
                attack.append(target)
                continue
            if attack:
                continue
            open_squares = list(filter(lambda o: isinstance(o, Empty), adj))
            candidates.extend(open_squares)
        if attack:
            target = sorted(attack, key=lambda u: (u.hp, u.y, u.x))[0]
            self.attack(target)
            return True
        if attack_only:
            return True
        if not candidates:
            return True
        paths = []
        for square in candidates:
            path = self.world.find_path(self, square)
            #print("Path from %r to %r: %s" %(self, square, path))
            if path is not None:
                paths.append(path)
        if not paths:
            return True
        min_len = min(map(len, paths))
        min_paths = filter(lambda p: len(p) == min_len, paths)
        min_paths = sorted(min_paths, key=lambda p: reading_order(p[-1]))
        chosen = min_paths[0]
        dest = chosen[0]
        self.world.move(self, dest.x, dest.y)
        return self.tick(attack_only=True)

class Goblin(Unit):
    marker = 'G'

class Elf(Unit):
    marker = 'E'

class World:
    def __init__(self):
        self.elves = []
        self.goblins = []
        self.map = []

    def add_object(self, x, y, obj):
        while len(self.map) <= y:
            self.map.append([])
        row = self.map[y]
        while len(row) <= x:
            row.append(Empty(x, y))
        row[x] = obj
        if isinstance(obj, Goblin):
            self.goblins.append(obj)
        elif isinstance(obj, Elf):
            self.elves.append(obj)

    def get_units(self):
        return self.elves + self.goblins

    def targets_for(self, unit):
        if isinstance(unit, Goblin):
            return self.elves
        elif isinstance(unit, Elf):
            return self.goblins

    def get_adjacent(self, obj):
        return list(filter(lambda u: u is not None, [
            self.map[obj.y - 1][obj.x] if obj.y >= 1 else None,
            self.map[obj.y + 1][obj.x] if obj.y < len(self.map) - 1 else None,
            self.map[obj.y][obj.x - 1] if obj.x >= 1 else None,
            self.map[obj.y][obj.x + 1] if obj.x < len(self.map[obj.y]) - 1 else None,
        ]))

    def dead_unit(self, unit):
        if isinstance(unit, Elf):
            self.elves = list(filter(lambda e: e is not unit, self.elves))
        elif isinstance(unit, Goblin):
            self.goblins = list(filter(lambda g: g is not unit, self.goblins))
        self.map[unit.y][unit.x] = Empty(unit.x, unit.y)

    def move(self, unit, x, y):
        assert isinstance(self.map[y][x], Empty)
        assert self.map[y][x] in self.get_adjacent(unit)
        self.map[unit.y][unit.x] = Empty(unit.x, unit.y)
        unit.x, unit.y = x, y
        self.map[y][x] = unit

    def find_path(self, src, dest):
        def get_adj(node):
            return list(filter(lambda o: isinstance(o, Empty) or o is src, self.get_adjacent(node)))
        weights = {}
        permanents = set()
        node = src
        curr_dist = 0
        while node != dest:
            weights[node] = curr_dist
            permanents.add(node)
            adj = get_adj(node)
            for a in adj:
                if a in permanents:
                    continue
                if a in weights:
                    weights[a] = min(weights[a], curr_dist + 1)
                else:
                    weights[a] = curr_dist + 1
            non_perms = list(filter(lambda e: e[0] not in permanents, weights.items()))
            if not non_perms:
                return None
            lowest = min(map(lambda e: e[1], non_perms))
            matching = filter(lambda e: e[1] == lowest, non_perms)
            ordered = sorted(matching, key=lambda e: reading_order(e[0]))
            closest = ordered[0]
            curr_dist += 1
            node = closest[0]
        permanents.add(dest)
        weights[dest] = curr_dist
        node = dest
        path = []
        while node != src:
            permanents.remove(node)
            path.append(node)
            dist = weights[node]
            perm_adj = list(filter(lambda a: a in permanents, get_adj(node)))
            lowest = min(map(lambda n: weights[n], perm_adj))
            matching = filter(lambda n: weights[n] == lowest, perm_adj)
            node = sorted(matching, key=reading_order)[0]
        return path[::-1]

    def tick(self):
        #self.print_world()
        for unit in sorted(self.get_units(), key=reading_order):
            if not unit.tick():
                return False
        return True

    def print_world(self):
        for row in self.map:
            print(''.join(map(str, row)))
        sys.stdout.flush()

    def combat_ended(self):
        return len(self.elves) == 0 or len(self.goblins) == 0

def to_component(char, world, x, y):
    if char == '#':
        return Wall(x, y)
    if char == '.':
        return Empty(x, y)
    if char == 'G':
        return Goblin(world, x, y)
    if char == 'E':
        return Elf(world, x, y)

if __name__ == '__main__':
    world = World()
    y = 0
    for line in sys.stdin:
        x = 0
        for c in line.strip():
            world.add_object(x, y, to_component(c, world, x, y))
            x += 1
        y += 1
    rounds = 0
    while not world.combat_ended():
        if world.tick():
            rounds += 1
    world.print_world()
    hit_points = sum(map(lambda u: u.hp, world.get_units()))
    print(rounds, hit_points, rounds * hit_points)
