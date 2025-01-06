from utils.data import *


def parse(data):
    locks = []
    keys = []
    for schematic in data.split("\n\n"):
        rows = schematic.splitlines()
        cols = list(zip(*rows))
        heights = [col.count("#") - 1 for col in cols]
        if all(val == "#" for val in rows[0]) and all(val == "." for val in rows[-1]):  # lock
            locks.append(heights)
        elif all(val == "." for val in rows[0]) and all(val == "#" for val in rows[-1]):
            keys.append(heights)
    return locks, keys


def part1(locks, keys):
    res = 0
    for lock in locks:
        for key in keys:
            for h1, h2 in zip(lock, key):
                if h1 + h2 > 5:
                    break
            else:
                res += 1
    return res


def part2():
    pass


test = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

data = get_and_write_data(25, 2024)
locks, keys = parse(data)
print_output(part1(locks, keys), part2())
