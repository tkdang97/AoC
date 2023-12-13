from utils.data import *
from utils.grid import neighbors4


def parse(data):
    res = []
    start = end = 0
    for i, line in enumerate(data.splitlines()):
        row = []
        for j, val in enumerate(line):
            if val == "S":
                start = (i, j)
                row.append(0)
            elif val == "E":
                end = (i, j)
                row.append(25)
            else:
                row.append(ord(val) - ord('a'))
        res.append(row)
    return res, start, end


def solve(grid, start, end):
    curr = start
    visited = set()
    steps = 0
    n = len(grid)
    m = len(grid[0])
    while curr:
        tmp = []
        for x, y in curr:
            visited.add((x, y))
            if (x, y) == end:
                return steps
            for dx, dy in neighbors4(x, y, n, m):
                if (dx, dy) not in visited and grid[dx][dy] <= grid[x][y] + 1:
                    visited.add((dx, dy))
                    tmp.append((dx, dy))
        steps += 1
        curr = tmp
    return steps


def part1(grid, start, end):
    return solve(grid, [start], end)


def part2(grid, end):
    starts = [(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == 0]
    return solve(grid, starts, end)


data = get_and_write_data(12, 2022)
grid, start, end = parse(data)
print_output(part1(grid, start, end), part2(grid, end))