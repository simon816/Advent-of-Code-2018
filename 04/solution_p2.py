import sys
import re

timere = re.compile('^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (wakes|falls|Guard #(\d+))')

class Guard:
    def __init__(self):
        self.days = {}
        self.counter = {}
        self.mincounts = [0] * 60

    def wake(self, y, m, d, M):
        start = self.counter[(y,m,d)]
        self.days.setdefault((y,m,d), 0)
        self.days[(y,m,d)] += (M - start)
        for i in range(start, M + 1):
            self.mincounts[i] += 1

    def sleep(self, y, m, d, M):
        self.counter[(y,m,d)] = M

    def total(self):
        return sum(self.days.values())

    def most(self):
        return max(enumerate(self.mincounts), key=lambda e: e[1])[0]

    def maxcount(self):
        return max(self.mincounts)

times = {}

guard = None
lines = list(sys.stdin)
lines = sorted(lines)
for line in lines:
    match = timere.match(line)
    y,m,d,H,M = map(int, match.group(*range(1, 6)))
    action, arg = match.group(6, 7)
    if arg:
        guard = arg
        times.setdefault(arg, Guard())
        continue
    if action == 'wakes':
        times[guard].wake(y, m, d, M)
    if action == 'falls':
        times[guard].sleep(y, m, d, M)

id, obj = max(times.items(), key=lambda i: i[1].maxcount())
print(int(id) * obj.most())

