from utils.data import *
from collections import Counter
from itertools import product


def parse(data):
    active = set()
    for x, row in enumerate(data.splitlines()):
        for y, val in enumerate(row):
            if val == "#":
                active.add((x, y, 0))
    return active


def simulate(curr_active, num_dimensions):
    active_neighbor_counts = Counter()
    for coord in curr_active:
        padded = coord if len(coord) == num_dimensions else coord + tuple([0] * (num_dimensions - len(coord)))
        for deltas in product((-1, 0, 1), repeat=num_dimensions):
            if any(d != 0 for d in deltas):
                active_neighbor_counts[tuple([c + dc for c, dc in zip(padded, deltas)])] += 1

    new_active = set()
    for coord, count in active_neighbor_counts.items():
        if coord in curr_active and (count == 2 or count == 3):  # active cube remains active
            new_active.add(coord)
        elif coord not in curr_active and count == 3:  # inactive cube becomes active
            new_active.add(coord)
    return new_active


def part1(active):
    curr_active = active
    for _ in range(6):
        curr_active = simulate(curr_active, 3)
    return len(curr_active)


def part2(active):
    curr_active = active
    for _ in range(6):
        curr_active = simulate(curr_active, 4)
    return len(curr_active)


test = """.#.
..#
###
"""

data = get_and_write_data(17, 2020)
active = parse(data)
print_output(part1(active), part2(active))
