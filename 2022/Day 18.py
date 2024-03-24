from utils.data import *


def parse(data):
    return list(map(lambda line: tuple(map(int, line.split(","))), data.splitlines()))


def get_neighbors(x, y, z):
    return (x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)


def part1(cubes):
    lava = set(cubes)
    total = 0
    for cube in cubes:
        for neighbor in get_neighbors(*cube):
            if neighbor not in lava:
                total += 1
    return total


def part2(cubes):
    min_x, min_y, min_z = map(lambda c: min(c) - 1, zip(*cubes))
    max_x, max_y, max_z = map(lambda c: max(c) + 1, zip(*cubes))
    water = set()
    lava = set(cubes)
    curr = {(min_x, min_y, min_z)}
    total = 0
    while curr:
        nxt = set()
        for cube in curr:
            water.add(cube)
            for x, y, z in get_neighbors(*cube):
                if (x, y, z) in lava:
                    total += 1
                elif min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z and (x, y, z) not in water:
                    nxt.add((x, y, z))
        curr = nxt
    return total


data = get_and_write_data(18, 2022)
cubes = parse(data)
print_output(part1(cubes), part2(cubes))
