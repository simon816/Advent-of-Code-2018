import sys

twice = 0
thrice = 0
for line in sys.stdin:
    uniques = set(line.strip())
    counts = dict([ (letter, line.count(letter)) for letter in uniques  ])
    unique_counts = set(counts.values())
    if 2 in unique_counts:
        twice += 1
    if 3 in unique_counts:
        thrice += 1
print (twice * thrice)
