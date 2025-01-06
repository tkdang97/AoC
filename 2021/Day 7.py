from utils.data import *
from statistics import mean, median
from math import ceil, floor


def parse(data):
    return list(map(int, data.strip().split(",")))


def part1(positions):
    med = int(median(positions))
    return sum(abs(p - med) for p in positions)


def part2(positions):
    # brute-force
    # min_cost = float("inf")
    # for pos in range(min(positions), max(positions) + 1):
    #     min_cost = min(min_cost, sum((abs(p - pos) * (abs(p - pos) + 1)) // 2 for p in positions))
    # return min_cost
    p1, p2 = ceil(mean(positions)), floor(mean(positions))
    return min(sum((abs(p - p1) * (abs(p - p1) + 1)) // 2 for p in positions),
               sum((abs(p - p2) * (abs(p - p2) + 1)) // 2 for p in positions))


data = get_and_write_data(7, 2021)
positions = parse(data)
print_output(part1(positions), part2(positions))