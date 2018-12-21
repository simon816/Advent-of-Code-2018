import sys

program = []

binding = None

for line in sys.stdin:
    opcode, *rest = line.split(' ')
    if opcode == '#ip':
        binding = int(rest[0])
    else:
        program.append((opcode,) + tuple(map(int, rest)))

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

regs = [0] * 6

ip = 0
count = 0
while True:
    if ip < 0 or ip >= len(program):
        break
    count += 1
    if ip == 28:
        print(regs[4])
        break
    opcode, A, B, C = program[ip]
    regs[binding] = ip
    run_insn(opcode, regs, A, B, C)
    ip = regs[binding]
    ip += 1
