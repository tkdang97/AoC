from utils.data import *
from operator import add, sub, mul, floordiv
import re

op_map = {"+": add, "-": sub, "*": mul, "/": floordiv}
reverse_ops = {"+": lambda a, b, lhs: a - b, "-": lambda a, b, lhs: a + b if lhs else b - a,
               "*": lambda a, b, lhs: a // b, "/": lambda a, b, lhs: a * b if lhs else b // a}


def parse(data):
    res = {}
    for line in data.splitlines():
        monkey, job = re.match(r"(\w+): (.+)", line).groups()
        if job.isdigit():
            res[monkey] = int(job)
        else:
            res[monkey] = re.match(r"(\w+) (.) (\w+)", job).groups()
    return res


def helper(monkeys, tgt):
    if isinstance(monkeys[tgt], int):
        return monkeys[tgt]
    m1, op, m2 = monkeys[tgt]
    return op_map[op](helper(monkeys, m1), helper(monkeys, m2))


def part1(monkeys):
    return helper(monkeys, "root")


def has_human(monkeys, monkey):
    if monkey == "humn":
        return True
    if isinstance(monkeys[monkey], int):
        return False
    m1, _, m2 = monkeys[monkey]
    return has_human(monkeys, m1) or has_human(monkeys, m2)


def helper_humn(monkeys, monkey, expected):
    m1, op, m2 = monkeys[monkey]
    humn_side = m2 if has_human(monkeys, m2) else m1
    lhs = m1 == humn_side
    other = helper(monkeys, m1) if not lhs else helper(monkeys, m2)
    next_val = reverse_ops[op](expected, other, lhs)
    if m1 == "humn" or m2 == "humn":
        return next_val
    return helper_humn(monkeys, humn_side, next_val)


def part2(monkeys):
    m1, _, m2 = monkeys["root"]
    humn_side = m2 if has_human(monkeys, m2) else m1
    target = helper(monkeys, m1) if m2 == humn_side else helper(monkeys, m2)
    return helper_humn(monkeys, humn_side, target)


data = get_and_write_data(21, 2022)
monkey_map = parse(data)
print_output(part1(monkey_map), part2(monkey_map))
