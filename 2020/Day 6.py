from utils.data import *


def parse(data):
    return [lines.splitlines() for lines in data.split("\n\n")]


def part1(groups):
    res = 0
    for group in groups:
        seen = set.union(*map(set, group))
        res += len(seen)
    return res


def part2(groups):
    res = 0
    for group in groups:
        seen = set.intersection(*map(set, group))
        res += len(seen)
    return res


test = """abc

a
b
c

ab
ac

a
a
a
a

b
"""

data = get_and_write_data(6, 2020)
groups = parse(data)
print_output(part1(groups), part2(groups))
