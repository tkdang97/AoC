from utils.data import *
from operator import add, mul
from math import prod


def parse(data):
    return [line + " " for line in data.splitlines()]


def resolve(values, ops, part2=False):
    tmp_vals = [values[0]]
    if part2:
        for val, op in zip(values[1:], ops):
            if op == "*":
                tmp_vals.append(val)
            else:
                tmp_vals.append(tmp_vals.pop() + val)
        return prod(tmp_vals)
    else:
        for val, op in zip(values[1:], ops):
            if op == "*":
                tmp_vals.append(tmp_vals.pop() * val)
            else:
                tmp_vals.append(tmp_vals.pop() + val)
        return tmp_vals[-1]


def evaluate(line, part2):
    values = []
    ops = []
    curr_num = 0
    i = 0
    while i < len(line):
        if line[i] in "+*":
            ops.append(line[i])
        elif line[i] == "(":
            res, end = evaluate(line[i + 1 :], part2)
            values.append(res)
            i += end
        elif line[i] == ")":
            if curr_num:
                values.append(curr_num)
            res = resolve(values, ops, part2)
            return res, i + 1
        elif line[i].isdigit():
            curr_num = curr_num * 10 + int(line[i])
        else:  # whitespace
            if curr_num > 0:
                values.append(curr_num)
                curr_num = 0
        i += 1
    return values[-1] if len(values) == 1 else resolve(values, ops, part2)


def part1(expressions):
    return sum(evaluate(line, False) for line in expressions)


def part2(expressions):
    return sum(evaluate(line, True) for line in expressions)


test = """5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
"""

data = get_and_write_data(18, 2020)
expressions = parse(data)
print_output(part1(expressions), part2(expressions))
