from utils.data import *
from collections import Counter
import re


def parse(data):
    return [tuple(map(int, tup)) for tup in re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", data)]


def solve(coordinates, enable_part2=False):
    count = Counter()
    for x1, y1, x2, y2 in coordinates:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                count[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                count[(x, y1)] += 1
        elif enable_part2:
            x_dir = -1 if x1 > x2 else 1
            y_dir = -1 if y1 > y2 else 1
            for i in range(0, abs(x1 - x2) + 1):
                count[(x1 + i * x_dir, y1 + i * y_dir)] += 1
    return sum(val > 1 for val in count.values())


def part1(coordinates):
    return solve(coordinates)


def part2(coordinates):
    return solve(coordinates, True)


data = get_and_write_data(5, 2021)
coords = parse(data)
print_output(part1(coords), part2(coords))
