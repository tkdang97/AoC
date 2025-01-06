from utils.data import *
from collections import Counter


def parse():
    claims = {}
    for line in data.splitlines():
        first, second = line.split(" @ ")
        claim = first[1:]
        coords, size = second.split(": ")
        x, y = map(int, coords.split(","))
        w, h = map(int, size.split("x"))
        claims[claim] = ((x, y), (w, h))
    return claims


def part1():
    counts = Counter()
    for (x, y), (w, h) in claims.values():
        for px in range(x, x + w):
            for py in range(y, y + h):
                counts[(px, py)] += 1
    return counts, sum(1 for val in counts.values() if val > 1)


def part2():
    for claim, ((x, y), (w, h)) in claims.items():
        if all(counts[(px, py)] == 1 for px in range(x, x + w) for py in range(y, y + h)):
            return claim


test = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""

data = get_and_write_data(3, 2018)
claims = parse()
counts, p1 = part1()
print_output(p1, part2())
