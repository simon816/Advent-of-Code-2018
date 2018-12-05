import sys

data = sys.stdin.read().strip()

changed = True
while changed:
    changed = False
    i = 0
    while i < len(data) - 1:
        if data[i].lower() == data[i+1].lower():
            if (data[i].islower() and data[i+1].isupper()) \
               or (data[i].isupper() and data[i+1].islower()):
                data = data[:i] + data[i+2:]
                changed = True
                continue
        i += 1

print(len(data))



