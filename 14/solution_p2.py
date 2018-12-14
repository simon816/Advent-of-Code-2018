import sys

scoreboard = [3, 7]

def get_next(pos):
    step = scoreboard[pos] + 1
    new_pos = step + pos
    if new_pos >= len(scoreboard):
        new_pos = new_pos % len(scoreboard)
    return new_pos

def num_to_list(val):
    digits = []
    while True:
        val, digit = divmod(val, 10)
        digits.append(digit)
        if val == 0: break
    return digits[::-1]

first_pos = 0
second_pos = 1

find = sys.stdin.read().strip()

while True:
    val = scoreboard[first_pos] + scoreboard[second_pos]
    digits = num_to_list(val)
    scoreboard.extend(digits)
    lpos = len(scoreboard) - len(digits) - len(find)
    possible = scoreboard[lpos:]
    if len(possible) >= len(find):
        pstr = ''.join(map(str, possible))
        pos = pstr.find(find)
        if pos != -1:
            print(lpos + pos)
            break
    first_pos = get_next(first_pos)
    second_pos = get_next(second_pos)
