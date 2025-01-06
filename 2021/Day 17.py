from utils.data import *
import re


def parse(data):
    min_x, max_x, min_y, max_y = map(int, re.search(r"x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", data).groups())
    return min_x, max_x, min_y, max_y


def part1(min_x, max_x, min_y, max_y):
    return ((abs(min_y) - 1) * abs(min_y)) // 2


def simulate(x, y, vx, vy, min_x, max_x, min_y, max_y):
    if x > max_x or y < min_y:  # overshot target area
        return 0
    if x >= min_x and y <= max_y:  # hit area
        return 1
    return simulate(x + vx, y + vy, vx - (vx > 0), vy - 1, min_x, max_x, min_y, max_y)


def part2(min_x, max_x, min_y, max_y):
    res = 0
    for vy in range(min_y, abs(min_y)):
        for vx in range(1, max_x + 1):
            res += simulate(0, 0, vx, vy, min_x, max_x, min_y, max_y)
    return res


data = get_and_write_data(17, 2021)
limits = parse(data)
print_output(part1(*limits), part2(*limits))
