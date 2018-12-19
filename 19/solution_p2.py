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
    'eqrr': lambda reg, A, B: 1 if reg[A] == reg[B] else 0,
}

### Stuff to simplify program

commutative = set([
    'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
    'setr', 'seti', 'eqir', 'eqri', 'eqrr'
])

def run_insn(name, reg, A, B, C):
    reg[C] = insns[name](reg, A, B)

constfn = {
    'addii': lambda A, B: A + B,
    'mulii': lambda A, B: A * B,
    'seti': lambda A, B: A
}

def const_resolve(opcode, A, B):
    fn = constfn.get(opcode)
    if not fn:
        return None
    return fn(A, B)

def to_string(opcode, A, B, C):
    if opcode == 'goto':
        return 'goto %d' % A
    if opcode == 'seti':
        return '[%d] <- %d' % (C, A)
    if opcode == 'setr':
        return '[%d] <- [%d]' % (C, A)
    if opcode == 'goto_addi':
        return 'goto [%d] + %d' % (A, B + 1)
    op = opcode
    if opcode.startswith('mul'):
        op = '*'
    elif opcode.startswith('add'):
        op = '+'
    elif opcode.startswith('ban'):
        op = '&'
    elif opcode.startswith('bor'):
        op = '|'
    elif opcode.startswith('gt'):
        op = '>'
    elif opcode.startswith('eq'):
        op = '=='
    if opcode[-1] == 'r':
        B = '[%d]' % B
    if opcode not in ['gtir', 'eqir']:
        A = '[%d]' % A
    return '[%d] <- %s %s %s' % (C, A, op, B)

for i in range(len(program)):
    opcode, A, B, C = program[i]
    # register access to B
    B_acc_reg = opcode[-1] == 'r' and opcode != 'setr'
    # register access to A
    A_acc_reg = opcode not in ['seti', 'gtir', 'eqir']

    if B == binding and B_acc_reg:
        # B is now immediate
        opcode = opcode[:-1] + 'i'
        B = i
        B_acc_reg = False

    if A == binding and A_acc_reg:
        # If A can be immediate, but B is not, and the opcode is commutative,
        # then switch A and B
        if opcode in commutative and B_acc_reg:
            A = B
            B = i
            # B is now immediate
            opcode = opcode[:-1] + 'i'
        else:
            # signify that A is immediate
            if opcode == 'setr':
                opcode = 'seti'
            else:
                opcode += 'i'
            A = i

    if C == binding:
        const = const_resolve(opcode, A, B)
        if const is not None:
            opcode = 'goto'
            A = const + 1 # +1 ip always increments
            B = C = ''
        else:
            opcode = 'goto_' + opcode

    print('%02d:' % i, to_string(opcode, A, B, C))
    if opcode.startswith('goto'):
        print()

regs = [0] * 6
regs[0] = 1

import math
def compute_sum_of_factors(target):
    lim = int(math.sqrt(target) + 0.5)
    res = 0
    for i in range(1, lim + 1):
        div, mod = divmod(target, i)
        if mod == 0:
            res += i
            if div != i:
                res += div
    return res

ip = 0
while True:
    if ip < 0 or ip >= len(program):
        break
    opcode, A, B, C = program[ip]
    regs[binding] = ip
    if ip == 4: # This is where the algorithm starts, testing
                # for the value in [B]
        print(compute_sum_of_factors(regs[B]))
        break
    run_insn(opcode, regs, A, B, C)
    ip = regs[binding]
    ip += 1
