import sys

scoreboard = [3, 7]

def get_next(pos):
    step = scoreboard[pos] + 1
    new_pos = step + pos
    if new_pos >= len(scoreboard):
        new_pos = new_pos % len(scoreboard)
    return new_pos

first_pos = 0
second_pos = 1

num_recipes = int(sys.stdin.read().strip())

while len(scoreboard) < num_recipes + 10:
    digits = []
    val = scoreboard[first_pos] + scoreboard[second_pos]
    while True:
        val, digit = divmod(val, 10)
        digits.append(digit)
        if val == 0: break
    scoreboard.extend(digits[::-1])
    first_pos = get_next(first_pos)
    second_pos = get_next(second_pos)

print(''.join(map(str, scoreboard[num_recipes:num_recipes + 10])))
