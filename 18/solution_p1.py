import sys

state = []
for line in sys.stdin:
    state.append(list(line.strip()))

for _ in range(10):
    new_state = []
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
            new_row.append(new_cell)
        new_state.append(new_row)
    state = new_state

num_trees = 0
num_lumberyard = 0
for row in state:
    num_trees += row.count('|')
    num_lumberyard += row.count('#')

print(num_trees * num_lumberyard)
