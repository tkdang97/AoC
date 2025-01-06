from utils.data import *
from itertools import pairwise
import re


def parse(data):
    levels = []
    for line in data.splitlines():
        levels.append(list(map(int, re.findall(r"\d+", line))))
    return levels


def is_safe(level):
    if level[1] == level[0] or abs(level[1] - level[0]) > 3:
        return False
    increasing = level[1] > level[0]
    safe = True
    for i in range(2, len(level)):
        if not (1 <= abs(level[i] - level[i - 1]) <= 3 and (level[i] > level[i - 1]) == increasing):
            safe = False
            break
    return safe


def part1(levels):
    return sum(map(is_safe, levels))


def part2(levels):
    res = 0
    for level in levels:
        if is_safe(level) or any(is_safe(level[:i] + level[i + 1:]) for i in range(0, len(level))):
            res += 1
    return res


test = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

data = get_and_write_data(2, 2024)
levels = parse(data)
print_output(part1(levels), part2(levels))
