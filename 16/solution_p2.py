import sys

gap = False

state = 0

data = []

program = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        if gap:
            state = 3
        gap = True
        continue
    gap = False
    if state == 0:
        before = tuple(map(int, map(str.strip, line[9:-1].split(','))))
        state = 1
    elif state == 1:
        insn = tuple(map(int, line.split(' ')))
        state = 2
    elif state == 2:
        after = tuple(map(int, map(str.strip, line[9:-1].split(','))))
        data.append((before, insn, after))
        state = 0
    elif state == 3:
        program.append(tuple(map(int, line.split(' '))))

insns = {
    'addr': lambda reg, A, B: reg[A] + reg[B],
    'addi': lambda reg, A, B: reg[A] + B,
    'mulr': lambda reg, A, B: reg[A] * reg[B],
    'muli': lambda reg, A, B: reg[A] * B,
    'banr': lambda reg, A, B: reg[A] & reg[B],
    'bani': lambda reg, A, B: reg[A] & B,
    'borr': lambda reg, A, B: reg[A] | reg[B],
    'bori': lambda reg, A, B: reg[A] | B,
    'setr': lambda reg, A, B: reg[A],
    'seti': lambda reg, A, B: A,
    'gtir': lambda reg, A, B: 1 if A > reg[B] else 0,
    'gtri': lambda reg, A, B: 1 if reg[A] > B else 0,
    'gtrr': lambda reg, A, B: 1 if reg[A] > reg[B] else 0,
    'eqir': lambda reg, A, B: 1 if A == reg[B] else 0,
    'eqri': lambda reg, A, B: 1 if reg[A] == B else 0,
    'eqrr': lambda reg, A, B: 1 if reg[A] == reg[B] else 0
}

def run_insn(name, reg, A, B, C):
    reg[C] = insns[name](reg, A, B)

could_be = {}

for before, insn, after in data:
    opnum, A, B, C = insn
    maybe = set()
    for opcode in insns.keys():
        reg = list(before)
        run_insn(opcode, reg, A, B, C)
        if tuple(reg) == after:
            maybe.add(opcode)
    if opnum not in could_be:
        could_be[opnum] = maybe
    else:
        could_be[opnum] = could_be[opnum] & maybe

definite = {}
while could_be:
    deletes = []
    for num, possible in could_be.items():
        for op in definite.values():
            possible.discard(op)
        if len(possible) == 1:
            definite[num] = possible.pop()
            deletes.append(num)
    for d in deletes:
        del could_be[d]

mapping = definite

reg = [0] * 4
for (opnum, A, B, C) in program:
    run_insn(mapping[opnum], reg, A, B, C)

print(reg[0])

