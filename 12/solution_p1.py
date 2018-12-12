import sys

init_state = list(sys.stdin.readline().strip()[len('initial state: '):])
sys.stdin.readline()

rules = {
    '.': [],
    '#': []
}

for line in sys.stdin:
    pattern, result = map(str.strip, line.split('=>'))
    c = pattern[2]
    rules[c].append((list(pattern[:2]), list(pattern[3:]), result))

def tick(state, lowest):
    new_state = list(state)
    shift_lower = 0
    for i in range(2, len(state)):
        matched = rules[state[i]]
        for rule in matched:
            left, right, res = rule
            if state[i-2:i] == left and state[i+1:i+3] == right:
                #print(i, left, state[i], right, res)
                new_state[i] = res
                if i < 2:
                    shift_lower += 1
                elif i >= len(state) - 3:
                    new_state.append('.')
                break
    for _ in range(shift_lower):
        new_state.insert(0, '.')
    return new_state, lowest - shift_lower
            

init_state.insert(0, '.')
init_state.insert(0, '.')
init_state.insert(0, '.')
init_state.extend(['.', '.'])
lowest = -3
state = init_state
for gen in range(20):
    state, lowest = tick(state, lowest)

tot = 0
for i in range(len(state)):
    pos = i + lowest
    if state[i] == '#':
        tot += pos

print(tot)
