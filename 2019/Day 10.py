from utils.data import *
from math import gcd
from collections import deque, defaultdict
from math import atan2, degrees


def parse(data):
    asteroids = set()
    for x, row in enumerate(data.splitlines()):
        for y, val in enumerate(row):
            if val == "#":
                asteroids.add((x, y))
    return asteroids


def part1():
    best = 0
    for x, y in asteroids:
        slopes = set()
        for nx, ny in asteroids:
            if not (x == nx and y == ny):
                dx, dy = x - nx, y - ny
                g = gcd(dx, dy)
                slopes.add((dx // g, dy // g))
        if len(slopes) > best:
            best = len(slopes)
    return best


def part2():
    final_slopes = {}
    final_x = final_y = 0
    best = 0
    for x, y in asteroids:
        slopes = defaultdict(list)
        for nx, ny in asteroids:
            if not (x == nx and y == ny):
                dx, dy = x - nx, y - ny
                g = gcd(dx, dy)
                slopes[(dx // g, dy // g)].append((nx, ny))
        if len(slopes) > best:
            best = len(slopes)
            final_slopes = slopes
            final_x = x
            final_y = y

    for key in final_slopes:
        final_slopes[key].sort(key=lambda x: (final_x - x[0]) ** 2 + (final_y - x[1]) ** 2)
        
    queue = deque(sorted(final_slopes.keys(), key=lambda x: (degrees(atan2(x[0], x[1])) - 90) % 360))

    x = y = 0
    for _ in range(200):
        coord = queue.popleft()
        x, y = final_slopes[coord].pop(0)
        if len(final_slopes[coord]) > 0:
            queue.append(coord)
    return y * 100 + x


test = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

data = get_and_write_data(10, 2019)
asteroids = parse(data)
print_output(part1(), part2())
