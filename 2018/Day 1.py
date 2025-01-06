from utils.data import *
from itertools import cycle


def parse():
    return list(map(int, data.splitlines()))


def part1():
    return sum(frequencies)


def part2():
    seen = {0}
    curr = 0
    for freq in cycle(frequencies):
        curr += freq
        if curr in seen:
            return curr
        seen.add(curr)
    print(seen)


test = """"""

data = get_and_write_data(1, 2018)
frequencies = parse()
print_output(part1(), part2())
