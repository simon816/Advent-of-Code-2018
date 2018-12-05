import sys
from string import ascii_letters

lower = ascii_letters[:26]
orig = sys.stdin.read().strip()

lengths = []
for remove in lower:
    data = orig.replace(remove, '').replace(remove.upper(), '')
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
    lengths.append(len(data))

print(min(lengths))



