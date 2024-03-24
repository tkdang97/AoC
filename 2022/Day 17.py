from utils.data import *
from itertools import cycle, zip_longest, count
from collections import deque, defaultdict


def parse(data, rock_string):
    # store the rocks as bit representations, with a 1 set for every position where a # is and from bottom to top

    rocks = []
    for rock in rock_string.split("\n\n"):
        rock_repr = []
        for line in rock.split("\n"):
            line_repr = 0
            for i, c in enumerate(line):
                if c == "#":
                    line_repr ^= 1 << (len(line) - i - 1)
            # shift the stone so that it is in the correct starting position, two units from the left wall
            # in the vertical chamber that is 7 units wide
            line_repr <<= (7 - len(line) - 2)
            rock_repr.append(line_repr)
        rocks.append(rock_repr[::-1])

    return data.strip(), rocks


def move_horizontal(rock, direction):
    match direction:
        case ">":
            if any(1 & row for row in rock):  # rock already touching right wall
                return rock
            return [row >> 1 for row in rock]

        case "<":
            if any((1 << 6) & row for row in rock):  # rock already touching left wall
                return rock
            return [row << 1 for row in rock]


def check_collisions(rock, chamber_spots):  # check for collision with other rocks or the floor
    for rock_row, chamber_row in zip_longest(rock, chamber_spots):
        if chamber_row is None:
            break
        if rock_row & chamber_row != 0:  # collision
            return True
    return False


def simulate_rock(jet_sequence, jet_idx, rock, chamber):
    for _ in range(3):  # rock spawns three units above highest rock, so no possible downwards collision for first three time steps
        rock = move_horizontal(rock, jet_sequence[jet_idx % len(jet_sequence)])
        jet_idx += 1
    curr_line = len(chamber) - 1
    chamber_spots = deque([chamber[curr_line] if curr_line > 0 else 0] + [0] * (len(rock) - 1))
    while True:
        new_rock = move_horizontal(rock, jet_sequence[jet_idx % len(jet_sequence)])  # horizontal movement first, check if move is possible
        jet_idx += 1
        if not check_collisions(new_rock, chamber[curr_line + 1: curr_line + 1 + len(rock)]):
            rock = new_rock
        if curr_line < 0 or check_collisions(rock, chamber_spots):  # rock can't move further down
            break
        chamber_spots.pop()
        curr_line -= 1
        chamber_spots.appendleft(chamber[curr_line] if curr_line >= 0 else 0)
    if len(chamber) <= curr_line + len(rock):
        chamber.extend([0] * ((curr_line + 1 + len(rock)) - len(chamber)))
    for i, row in enumerate(rock):
        chamber[curr_line + 1 + i] ^= row
    return jet_idx


def part1(jet_sequence, rock_sequence):
    chamber = []
    jet_idx = 0
    for i in range(2022):
        jet_idx = simulate_rock(jet_sequence, jet_idx, rock_sequence[i % len(rock_sequence)], chamber)
    return len(chamber)


def part2(jet_sequence, rock_sequence):
    chamber = []
    jet_idx = 0
    cycle_len = height_diff = 0
    seen = dict()
    init_height = init_offset = 0
    target = 1000000000000
    vals = []
    for i in count(0):
        jet_idx = simulate_rock(jet_sequence, jet_idx, rock_sequence[i % len(rock_sequence)], chamber)
        #  We use as a lookup key (last 8 rows of the chamber, position in jet sequence, position in rock sequence)
        key = (tuple(chamber[-8:]), jet_idx % len(jet_sequence), i % len(rock_sequence))
        if key in seen:
            vals[seen[key]].append((i, len(chamber)))
            if len(vals[seen[key]]) >= 3:  # check for two full cycles until third encounter for extra security
                cycle_len = vals[seen[key]][-1][0] - vals[seen[key]][-2][0]
                height_diff = vals[seen[key]][-1][1] - vals[seen[key]][-2][1]
                init_offset, init_height = vals[seen[key]][0]
                break
        else:
            seen[key] = i
            vals.append([(i, len(chamber))])
    num_cycles = (target - init_offset) // cycle_len
    res_height = num_cycles * height_diff + init_height
    remaining_steps = target - (num_cycles * cycle_len) - init_offset - 1  # -1 because we start counting from 0
    res_height += vals[init_offset + remaining_steps][-1][1] - vals[init_offset][-2][1]
    return res_height


rock_string = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""
data = get_and_write_data(17, 2022)
jet_sequence, rock_sequence = parse(data, rock_string)
print_output(part1(jet_sequence, rock_sequence), part2(jet_sequence, rock_sequence))
