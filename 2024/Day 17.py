from utils.data import *
import re


def parse(data):
    numbers = list(map(int, re.findall("\d+", data)))
    registers = numbers[:3]
    program = numbers[3:]
    return registers, program


def execute_op(opcode, registers, operand, pos, out):
    combo = operand
    if combo > 3:
        combo = registers[combo - 4]
    match opcode:
        case 0:
            registers[0] = registers[0] // (2**combo)
        case 1:
            registers[1] ^= operand
        case 2:
            registers[1] = combo % 8
        case 3:
            if registers[0] != 0:
                return operand
        case 4:
            registers[1] ^= registers[2]
        case 5:
            out.append(combo % 8)
        case 6:
            registers[1] = registers[0] // (2**combo)
        case 7:
            registers[2] = registers[0] // (2**combo)
    return pos + 2


def part1(registers, program):
    n = len(program) - 1
    cpy = registers.copy()
    pos = 0
    res = []
    while pos < n:
        pos = execute_op(program[pos], cpy, program[pos + 1], pos, res)
    return ",".join(map(str, res))


def part2(registers, program):
    n = len(program) - 1
    check = [(1, 0)]
    for i, next_a in check:
        for a in range(next_a, next_a + 8):
            cpy = registers.copy()
            cpy[0] = a
            pos = 0
            res = []
            while pos < n:
                pos = execute_op(program[pos], cpy, program[pos + 1], pos, res)
            if res == program[-i:]:
                check.append((i + 1, a * 8))
                if i == len(program):
                    return a


test = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

data = get_and_write_data(17, 2024)
registers, program = parse(data)
print_output(part1(registers, program), part2(registers, program))
