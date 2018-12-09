import sys
import re

players, lastworth = \
         map(int, re.match('^(\d+) players; last marble is worth (\d+) points',
                  sys.stdin.read()).groups())

n_marbles = (lastworth * 100) + 1

scores = [0] * players

class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

    def seek(self, val):
        if val == 0:
            return self
        if val < 0:
            return self.prev.seek(val + 1)
        else:
            return self.next.seek(val - 1)

    def insert_ahead(self, val):
        new = Node(val)
        new.next = self.next
        self.next.prev = new
        new.prev = self
        self.next = new
        return new

    def unlink(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.next

    def __repr__(self):
        return 'Node(%r)' % self.val

curr = None
player = 0
for worth in range(n_marbles):
    if worth == 0:
        curr = Node(0)
    elif worth == 1:
        new = Node(1)
        curr.next = new
        curr.prev = new
        new.next = curr
        new.prev = curr
        curr = new
    elif worth != 0 and worth % 23 == 0:
        scores[player] += worth
        curr = curr.seek(-7)
        scores[player] += curr.val
        curr = curr.unlink()
    else:
        curr = curr.seek(1)
        curr = curr.insert_ahead(worth)
    player = (player + 1) % players

print(max(scores))
