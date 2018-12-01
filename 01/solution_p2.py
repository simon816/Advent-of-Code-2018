import sys
lines = sys.stdin.readlines()
seen = set([])

value = 0
found = False
while not found:
    for line in lines:
        value = eval('value + ' + line)
        if value in seen:
            print(value)
            found = True
            break
        seen.add(value)
