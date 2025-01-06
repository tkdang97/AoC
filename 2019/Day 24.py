from utils.data import *
from utils.grid import neighbors4


def parse(data):
    return data.splitlines()


def step(grid):
    res = []
    m, n = 5, 5
    for x, row in enumerate(grid):
        new_row = ""
        for y, val in enumerate(row):
            bugs = sum(grid[nx][ny] == "#" for nx, ny in neighbors4(x, y, m, n))
            if val == "#":
                if bugs == 1:
                    new_row += "#"
                else:
                    new_row += "."
            else:
                if bugs == 1 or bugs == 2:
                    new_row += "#"
                else:
                    new_row += "."
        res.append(new_row)
    return res


def part1():
    seen = set()
    curr = grid
    while True:
        check = "\n".join(curr)
        if check in seen:
            return sum(2 ** (x * 5 + y) for x, row in enumerate(curr) for y, val in enumerate(row) if val == "#")
        seen.add(check)
        curr = step(curr)


def count_bugs(bugs, x, y, z):
    count = 0
    if x == 0 and (1, 2, z - 1) in bugs:
        count += 1
    if x == 4 and (3, 2, z - 1) in bugs:
        count += 1
    if y == 0 and (2, 1, z - 1) in bugs:
        count += 1
    if y == 4 and (2, 3, z - 1) in bugs:
        count += 1

    if (x, y) == (1, 2):
        count += sum((0, Y, z + 1) in bugs for Y in range(5))
    if (x, y) == (3, 2):
        count += sum((4, Y, z + 1) in bugs for Y in range(5))
    if (x, y) == (2, 1):
        count += sum((X, 0, z + 1) in bugs for X in range(5))
    if (x, y) == (2, 3):
        count += sum((X, 4, z + 1) in bugs for X in range(5))

    for dx, dy in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        nx, ny = x + dx, y + dy
        if (nx, ny, z) in bugs:
            count += 1
    return count


def step2(bugs):
    next_bugs = set()
    min_z, max_z = min(c[2] for c in bugs), max(c[2] for c in bugs)
    for z in range(min_z - 1, max_z + 2):
        for x in range(5):
            for y in range(5):
                if x == 2 and y == 2:
                    continue
                neighbor_bugs = count_bugs(bugs, x, y, z)
                if (x, y, z) in bugs:
                    if neighbor_bugs == 1:
                        next_bugs.add((x, y, z))
                elif neighbor_bugs == 1 or neighbor_bugs == 2:
                    next_bugs.add((x, y, z))
    return next_bugs


def part2():
    bugs = {(x, y, 0) for x, row in enumerate(grid) for y, val in enumerate(row) if val == "#"}
    for _ in range(200):
        bugs = step2(bugs)
    return len(bugs)


test = """....#
#..#.
#..##
..#..
#...."""

data = get_and_write_data(24, 2019)
grid = parse(data)
print_output(part1(), part2())
