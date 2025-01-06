from utils.data import *
from itertools import pairwise


def parse(data):
    return list(map(int, data.splitlines()))


def part1(depths):
    return sum(x2 > x1 for x1, x2 in pairwise(depths))


def part2(depths):
    triplets = zip(depths, depths[1:], depths[2:])
    return sum(sum(x2) > sum(x1) for x1, x2 in pairwise(triplets))


data = get_and_write_data(1, 2021)
depths = parse(data)
print_output(part1(depths), part2(depths))
