from utils.data import *


def parse(data):
    return [line.split() for line in data.splitlines()]


def simulate(instructions):
    acc = 0
    seen = set()
    curr = 0
    success = True
    while curr < len(instructions):
        if curr in seen:
            success = False
            break
        seen.add(curr)
        op, arg = instructions[curr]
        if op == "jmp":
            curr += int(arg)
            continue
        if op == "acc":
            acc += int(arg)
        curr += 1

    return acc, success


def part1(instructions):
    return simulate(instructions)[0]


def part2(instructions):
    for i in range(len(instructions)):
        prev = instructions[i][0]
        if prev == "acc":
            continue
        instructions[i][0] = "jmp" if prev == "nop" else "nop"
        acc, success = simulate(instructions)
        if success:
            return acc
        instructions[i][0] = prev


test = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

data = get_and_write_data(8, 2020)
instructions = parse(data)
print_output(part1(instructions), part2(instructions))
