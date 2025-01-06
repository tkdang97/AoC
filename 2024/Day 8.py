from utils.data import *
from collections import defaultdict
from itertools import permutations


def parse(data):
    grid = [list(row) for row in data.splitlines()]
    antennas = defaultdict(list)
    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            if node != ".":
                antennas[node].append((i, j))
    return antennas, len(grid), len(grid[0])


def part1(antennas, m, n):
    locations = set()
    for coords in antennas.values():
        if len(coords) > 1:
            for (x1, y1), (x2, y2) in permutations(coords, 2):
                x_diff = x2 - x1
                y_diff = y2 - y1
                candidate = (x1 - x_diff, y1 - y_diff)
                if 0 <= candidate[0] < m and 0 <= candidate[1] < n:
                    locations.add(candidate)
    return len(locations)


def part2(antennas, m, n):
    locations = set()
    for coords in antennas.values():
        if len(coords) > 1:
            for (x1, y1), (x2, y2) in permutations(coords, 2):
                x_diff = x1 - x2
                y_diff = y1 - y2
                curr_pos = (x1, y1)
                while True:
                    curr_pos = (curr_pos[0] - x_diff, curr_pos[1] - y_diff)
                    if 0 <= curr_pos[0] < m and 0 <= curr_pos[1] < n:
                        locations.add(curr_pos)
                    else:
                        break
                locations.add((x2, y2))
    return len(locations)


test = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

data = get_and_write_data(8, 2024)
parsed_data = parse(data)
print_output(part1(*parsed_data), part2(*parsed_data))
