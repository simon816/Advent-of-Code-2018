import sys


mem = {}

def distance(p1, p2):
    if (p2, p1) in mem:
        return mem[p2, p1]
    if (p1, p2) in mem:
        return mem[p1, p2]
    dist = 0
    for i, d in enumerate(p1):
        dist += abs(d - p2[i])
    mem[p1, p2] = dist
    return dist

class Group:

    def __init__(self, starting=None):
        if starting is None:
            self.members = []
        else:
            self.members = [starting]

    def can_join(self, point):
        for member in self.members:
            if distance(member, point) <= 3:
                return True
        return False

    def append(self, point):
        self.members.append(point)

    def can_merge(self, other):
        for member in other.members:
            if self.can_join(member):
                return True
        return False

    def merge(self, other):
        self.members.extend(other.members)

groups = []

for line in sys.stdin:
    coord = tuple(map(int, line.strip().split(',')))
    joined = False
    for group in groups:
        if group.can_join(coord):
            group.append(coord)
            joined = True
            break
    if not joined:
        groups.append(Group(coord))

while True:
    new_groups = set()
    rem = set()
    changed = False
    for g1 in groups:
        if g1 in rem:
            continue
        for g2 in groups:
            if g1 is g2:
                continue
            if g1.can_merge(g2):
                g1.merge(g2)
                rem.add(g2)
                changed = True
        new_groups.add(g1)
    groups = new_groups - rem
    if not changed:
        break


print(len(groups))
