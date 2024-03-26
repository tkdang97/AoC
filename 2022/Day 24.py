from utils.data import *


directions = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}


def parse(data):
    lines = data.splitlines()
    start, end = (lines[0].find("."), 0), (lines[-1].find("."), len(lines) - 1)
    max_x, max_y = len(lines[0]) - 2, len(lines) - 2
    blizzards = []
    for i, line in enumerate(lines[1: -1], 1):
        for j, symbol in enumerate(line[1: -1], 1):
            if symbol in directions:
                blizzards.append((j, i, symbol))
    return start, end, max_x, max_y, blizzards


def move_blizzards(blizzards, max_x, max_y):
    res = []
    for x, y, direction in blizzards:
        if x == 1 and direction == "<":  # hitting left wall
            res.append((max_x, y, direction))
        elif x == max_x and direction == ">":  # right wall
            res.append((1, y, direction))
        elif y == 1 and direction == "^":  # top wall
            res.append((x, max_y, direction))
        elif y == max_y and direction == "v":  # bottom wall
            res.append((x, 1, direction))
        else:  # normal movement
            res.append((x + directions[direction][0], y + directions[direction][1], direction))
    return res


def move_expedition(blizzards, max_x, max_y, x, y, end):
    res = {(x, y)}
    for dx, dy in directions.values():
        if (1 <= x + dx <= max_x and 1 <= y + dy <= max_y) or (x + dx, y + dy) == end:
            res.add((x + dx, y + dy))
    return res - blizzards


def simulate(start, end, count, max_x, max_y, blizzards):
    curr = {start}
    blizz = blizzards.copy()
    while curr and end not in curr:
        count += 1
        blizz = move_blizzards(blizz, max_x, max_y)
        blizz_set = set([(x, y) for x, y, _ in blizz])
        next_pos = set()
        for x, y in curr:
            next_pos |= move_expedition(blizz_set, max_x, max_y, x, y, end)
        curr = next_pos
    return count, blizz


def part1(start, end, max_x, max_y, blizzards):
    return simulate(start, end, 0, max_x, max_y, blizzards)[0]


def part2(start, end, max_x, max_y, blizzards):
    count, blizz = simulate(start, end, 0, max_x, max_y, blizzards)  # first forward pass
    count, blizz = simulate(end, start, count, max_x, max_y, blizz)  # backward pass
    return simulate(start, end, count, max_x, max_y, blizz)[0]       # last forward pass


data = get_and_write_data(24, 2022)
parsed = parse(data)
print_output(part1(*parsed), part2(*parsed))
