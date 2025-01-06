from utils.data import *


def parse(data):
    dirs = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}
    wire1, wire2 = data.splitlines()
    x = y = t = 0
    positions1 = {}
    for instruction in wire1.split(","):
        dir = instruction[0]
        steps = instruction[1:]
        dx, dy = dirs[dir]
        for _ in range(int(steps)):
            x += dx
            y += dy
            t += 1
            if (x, y) not in positions1:
                positions1[(x, y)] = t

    x = y = t = 0
    positions2 = {}
    for instruction in wire2.split(","):
        dir = instruction[0]
        steps = instruction[1:]
        dx, dy = dirs[dir]
        for _ in range(int(steps)):
            x += dx
            y += dy
            t += 1
            if (x, y) not in positions2:
                positions2[(x, y)] = t

    return positions1, positions2


def part1(positions1, positions2):
    return min(abs(x) + abs(y) for x, y in set(positions1.keys()) & set(positions2.keys()))


def part2(positions1, positions2):
    return min(positions1[coord] + positions2[coord] for coord in set(positions1.keys()) & set(positions2.keys()))


test = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""

data = get_and_write_data(3, 2019)
positions = parse(data)
print_output(part1(*positions), part2(*positions))
