from utils.data import *


def parse(data):
    rights = set()
    downs = set()
    grid = data.splitlines()
    for x, row in enumerate(grid):
        for y, val in enumerate(row):
            if val == ">":
                rights.add((x, y))
            elif val == "v":
                downs.add((x, y))
    return rights, downs, len(grid), len(grid[0])


def part1(rights, downs, m, n):
    moved = 1
    res = 0
    while moved > 0:
        curr_moved = 0
        new_rights = set()
        for x, y in rights:
            nx, ny = x, (y + 1) % n
            if (nx, ny) not in rights and (nx, ny) not in downs:
                new_rights.add((nx, ny))
                curr_moved += 1
            else:
                new_rights.add((x, y))
        new_downs = set()
        for x, y in downs:
            nx, ny = (x + 1) % m, y
            if (nx, ny) not in new_rights and (nx, ny) not in downs:
                new_downs.add((nx, ny))
                curr_moved += 1
            else:
                new_downs.add((x, y))
        rights = new_rights
        downs = new_downs
        moved = curr_moved
        res += 1
    return res


def part2():
    pass


test = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""

data = get_and_write_data(25, 2021)
rights, downs, m, n = parse(data)
print_output(part1(rights, downs, m, n), part2())
