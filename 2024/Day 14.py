from utils.data import *
import re
from math import prod
from itertools import count


def parse(data):
    pattern = r"p=(\-?\d+),(\-?\d+) v=(\-?\d+),(\-?\d+)"
    return [list(map(int, line)) for line in re.findall(pattern, data)]


def print_grid(pos, width, height):
    grid = [[0] * width for _ in range(height)]
    for x, y in pos:
        grid[y][x] += 1
    for row in grid:
        print("".join("." if val == 0 else "*" for val in row))


def part1(robots, width=101, height=103, seconds=100):
    end_positions = []
    for robot in robots:
        curr_x, curr_y, dx, dy = robot
        for _ in range(seconds):
            curr_x = (curr_x + dx) % width
            curr_y = (curr_y + dy) % height
        end_positions.append((curr_x, curr_y))
    mid_x = width // 2
    mid_y = height // 2
    counts = [0] * 4
    for x, y in end_positions:
        if x < mid_x and y < mid_y:
            counts[0] += 1
        elif x > mid_x and y < mid_y:
            counts[1] += 1
        elif x < mid_x and y > mid_y:
            counts[2] += 1
        elif x > mid_x and y > mid_y:
            counts[3] += 1
    return prod(counts)


def part2(robots, width=101, height=103):
    curr_positions = robots.copy()
    for second in count(1):
        curr_positions = [((x + dx) % width, (y + dy) % height, dx, dy) for x, y, dx, dy in curr_positions]
        if len(set((x, y) for x, y, _, _ in curr_positions)) == len(curr_positions):
            return second


test = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

data = get_and_write_data(14, 2024)
robots = parse(data)
print_output(part1(robots), part2(robots))
