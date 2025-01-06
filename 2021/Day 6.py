from utils.data import *
from collections import Counter


def parse(data):
    return list(map(int, data.strip().split(",")))


def solve(ages, days):
    counts = Counter(ages)
    for day in range(days):
        counts[(day + 7) % 9] += counts[day % 9]
    return sum(counts.values())


def part1(ages):
    return solve(ages, 80)


def part2(ages):
    return solve(ages, 256)


data = get_and_write_data(6, 2021)
ages = parse(data)
print_output(part1(ages), part2(ages))