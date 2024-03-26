from utils.data import *
from collections import Counter
from itertools import count


directions = {"N": (0, -1), "NW": (-1, -1), "NE": (1, -1), "E": (1, 0)
              , "W": (-1, 0), "S": (0, 1), "SW": (-1, 1), "SE": (1, 1)}


def parse(data):
    res = set()
    for i, line in enumerate(data.splitlines()):
        for j, tile in enumerate(line):
            if tile == "#":
                res.add((j, i))
    return res


def check_surroundings(positions, x, y):
    for dx, dy in directions.values():
        if (x + dx, y + dy) in positions:
            return True
    return False


def valid_move(positions, x, y, direction):
    match direction:
        case "N":
            return not any((x + dx, y + dy) in positions for dx, dy in (directions["N"], directions["NE"], directions["NW"]))
        case "S":
            return not any((x + dx, y + dy) in positions for dx, dy in (directions["S"], directions["SE"], directions["SW"]))
        case "W":
            return not any((x + dx, y + dy) in positions for dx, dy in (directions["W"], directions["NW"], directions["SW"]))
        case "E":
            return not any((x + dx, y + dy) in positions for dx, dy in (directions["E"], directions["NE"], directions["SE"]))
        case _:
            raise ValueError("Not a valid direction")


def simulate(positions, rounds):
    order = ["N", "S", "W", "E"]
    curr = 0
    coords = positions.copy()
    for r in count():
        if rounds and r >= rounds:
            break
        proposed = {}
        new_coords = set()
        for x, y in coords:
            if check_surroundings(coords, x, y):
                move = ""
                for i in range(4):
                    direction = order[(curr + i) % 4]
                    if valid_move(coords, x, y, direction):
                        move = direction
                        break
                proposed[(x, y)] = (x + directions[move][0], y + directions[move][1]) if move else (x, y)
            else:
                proposed[(x, y)] = (x, y)
        counts = Counter(proposed.values())
        invalid = {coord for coord in counts if counts[coord] > 1}  # overlapping moves
        for coord, new_coord in proposed.items():
            if new_coord in invalid:
                new_coords.add(coord)
            else:
                new_coords.add(new_coord)
        if coords == new_coords:
            return coords, r + 1
        coords = new_coords
        curr += 1
    return coords, 0


def part1(positions):
    end_pos, _ = simulate(positions, 10)
    min_x, min_y = map(min, zip(*end_pos))
    max_x, max_y = map(max, zip(*end_pos))
    area = (max_x + 1 - min_x) * (max_y + 1 - min_y)
    return area - len(positions)


def part2(positions):
    _, end_round = simulate(positions, 0)
    return end_round


data = get_and_write_data(23, 2022)
positions = parse(data)
print_output(part1(positions), part2(positions))
