from utils.data import *
import re
from itertools import pairwise
import copy


def parse(data):
    blocked = set()
    max_y = -1
    for line in data.splitlines():
        for (x0, y0), (x1, y1) in pairwise(map(lambda v: tuple(map(int, v)), re.findall(r"(\d+),(\d+)", line))):
            if x0 == x1:
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    blocked.add((x0, y))
            else:
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    blocked.add((x, y0))
            max_y = max(max_y, y0, y1)

    max_y += 2  # for part 2
    for x in range(500 - max_y - 1, 500 + max_y + 1):  # since you can at most move 1 left/right per move down just fill to this width
        blocked.add((x, max_y))
    return blocked, max_y


def solve(blocked, max_y, p1=True):
    count = 0
    tmp = copy.deepcopy(blocked)
    while True:
        if not p1 and (500, 0) in tmp:
            return count

        x, y = 500, 0
        while True:
            if p1 and y >= max_y - 1:
                return count

            for dx in (0, -1, 1):
                if (x + dx, y + 1) not in tmp:
                    x, y = x + dx, y + 1
                    break
            else:
                tmp.add((x, y))
                break
        count += 1


def part1(blocked, max_y):
    return solve(blocked, max_y)


def part2(blocked):
    return solve(blocked, 0, False)


data = get_and_write_data(14, 2022)
blocked, max_y = parse(data)
print_output(part1(blocked, max_y), part2(blocked))
