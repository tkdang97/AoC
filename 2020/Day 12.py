from utils.data import *


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
cardinals = {"E": 0, "S": 1, "W": 2, "N": 3}


def parse(data):
    res = []
    for line in data.splitlines():
        val = int(line[1:])
        res.append((line[0], val))
    return res


def part1(instructions):
    x, y = 0, 0
    facing = 0
    for instruction, val in instructions:
        match instruction:
            case "L":
                facing = (facing - (val // 90)) % 4
            case "R":
                facing = (facing + (val // 90)) % 4
            case "F":
                x += val * directions[facing][0]
                y += val * directions[facing][1]
            case _:
                x += val * directions[cardinals[instruction]][0]
                y += val * directions[cardinals[instruction]][1]
    return abs(x) + abs(y)


def part2(instructions):
    x_ship, y_ship = 0, 0
    x_way, y_way = -1, 10
    for instruction, val in instructions:
        match instruction:
            case "L":
                for _ in range(val // 90):
                    x_way, y_way = -1 * y_way, x_way
            case "R":
                for _ in range(val // 90):
                    x_way, y_way = y_way, -1 * x_way
            case "F":
                x_ship += val * x_way
                y_ship += val * y_way
            case _:
                x_way += val * directions[cardinals[instruction]][0]
                y_way += val * directions[cardinals[instruction]][1]
    return abs(x_ship) + abs(y_ship)


test = """F10
N3
F7
R90
F11
"""

data = get_and_write_data(12, 2020)
instructions = parse(data)
print_output(part1(instructions), part2(instructions))
