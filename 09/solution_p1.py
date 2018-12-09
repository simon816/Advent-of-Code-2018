import sys
import re

players, lastworth = \
         map(int, re.match('^(\d+) players; last marble is worth (\d+) points',
                  sys.stdin.read()).groups())

n_marbles = lastworth + 1

scores = [0] * players

circle = []

curr = -2 # +2 makes this 0

player = 0
for worth in range(n_marbles):
    if worth != 0 and worth % 23 == 0:
        scores[player] += worth
        curr -= 7
        if curr < 0:
            curr += len(circle)
        scores[player] += circle.pop(curr)
    else:
        curr = curr + 2
        if curr > len(circle):
            curr -= len(circle)
        if curr == len(circle):
            circle.append(worth)
        else:
            circle.insert(curr, worth)
    player = (player + 1) % players

print(max(scores))
