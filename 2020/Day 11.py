from utils.data import *
from utils.grid import neighbors8
from copy import deepcopy


def parse(data):
    return list(map(list, data.splitlines()))


def simulate_round(grid, part2=False):
    res = []
    m, n = len(grid), len(grid[0])
    num_changes = 0
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    for i, row in enumerate(grid):
        new_row = []
        for j, val in enumerate(row):
            if val == ".":
                new_row.append(".")
            else:
                count = 0
                if part2:
                    for dx, dy in directions:
                        visible = "."
                        x, y = i + dx, j + dy
                        while 0 <= x < m and 0 <= y < n:
                            if grid[x][y] != ".":
                                visible = grid[x][y]
                                break
                            x, y = x + dx, y + dy
                        if visible == "#":
                            count += 1
                else:
                    for x, y in neighbors8(i, j, m, n):
                        if grid[x][y] == "#":
                            count += 1
                if val == "L":
                    if count == 0:
                        num_changes += 1
                        new_row.append("#")
                    else:
                        new_row.append("L")
                else:
                    if (part2 and count >= 5) or (not part2 and count >= 4):
                        num_changes += 1
                        new_row.append("L")
                    else:
                        new_row.append("#")
        res.append(new_row)

    return res, num_changes


def part1(grid):
    num_changes = 1
    curr = deepcopy(grid)
    while num_changes > 0:
        curr, num_changes = simulate_round(curr)
    return sum(row.count("#") for row in curr)


def part2(grid):
    num_changes = 1
    curr = deepcopy(grid)
    while num_changes > 0:
        curr, num_changes = simulate_round(curr, True)
        # print("\n".join("".join(row) for row in curr), end="\n\n")
    return sum(row.count("#") for row in curr)


test = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

data = get_and_write_data(11, 2020)
grid = parse(data)
print_output(part1(grid), part2(grid))
