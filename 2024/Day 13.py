from utils.data import *
import re
from functools import cache
import numpy as np


def parse(data):
    pattern = r".*X\+(\d+).*Y\+(\d+)\n.*X\+(\d+).*Y\+(\d+)\n.*X=(\d+).*Y=(\d+)"
    return [list(map(int, game)) for game in re.findall(pattern, data)]


def solve(x1, y1, x2, y2, xgoal, ygoal):
    matrix = np.array([[x1, x2], [y1, y2]])
    goal = np.array([xgoal, ygoal])
    res = np.round(np.linalg.solve(matrix, goal))
    return round(res @ (3, 1)) if (goal == res @ matrix.T).all() else 0


def part1(games):
    total = 0
    for x1, y1, x2, y2, xgoal, ygoal in games:
        total += solve(x1, y1, x2, y2, xgoal, ygoal)

    return total


def part2(games):
    total = 0
    for x1, y1, x2, y2, xgoal, ygoal in games:
        xgoal += 10000000000000
        ygoal += 10000000000000

        total += solve(x1, y1, x2, y2, xgoal, ygoal)

    return total


test = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

data = get_and_write_data(13, 2024)
games = parse(data)
print_output(part1(games), part2(games))
