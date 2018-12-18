import sys

state = []
for line in sys.stdin:
    state.append(tuple(line.strip()))

seen_map = {}
value_list = []

for tick in range(1000000000):
    new_state = []
    num_trees = 0
    num_lumberyard = 0
    for y in range(len(state)):
        row = state[y]
        other_rows = []
        if y > 0:
            other_rows.append(state[y-1])
        if y < len(state) - 1:
            other_rows.append(state[y+1])
        new_row = []
        for x in range(len(row)):
            cell = row[x]
            adjacent = []
            if x > 0:
                adjacent.append(row[x-1])
                adjacent.extend(other[x-1] for other in other_rows)
            if x < len(row) - 1:
                adjacent.append(row[x+1])
                adjacent.extend(other[x+1] for other in other_rows)
            adjacent.extend(other[x] for other in other_rows)
            new_cell = cell
            if cell == '.':
                if adjacent.count('|') >= 3:
                    new_cell = '|'
            elif cell == '|':
                if adjacent.count('#') >= 3:
                    new_cell = '#'
            elif cell == '#':
                if adjacent.count('#') == 0 or adjacent.count('|') == 0:
                    new_cell = '.'
            if new_cell == '|':
                num_trees += 1
            elif new_cell == '#':
                num_lumberyard += 1
            new_row.append(new_cell)
        new_state.append(tuple(new_row))
    state = new_state
    value_list.append(num_trees * num_lumberyard)
    h = hash(tuple(state))
    if h in seen_map:
        start_tick, end_tick = seen_map[h], tick
        cycle = end_tick - start_tick
        # off by one for some reason
        print(value_list[start_tick + ((1000000000 - start_tick - 1) % cycle)])
        break
    seen_map[h] = tick
