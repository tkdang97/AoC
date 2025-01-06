from utils.data import *
from utils.grid import neighbors4


def parse(data):
    return [list(map(int, line)) for line in data.splitlines()]


def part1(grid):
    m, n = len(grid), len(grid[0])

    def rec(x, y):
        if grid[x][y] == 9:
            return {(x, y)}
        res = set()
        for nx, ny in neighbors4(x, y, m, n):
            if grid[nx][ny] == grid[x][y] + 1:
                res |= rec(nx, ny)
        return res

    total = 0
    for x, row in enumerate(grid):
        for y, val in enumerate(row):
            if val == 0:
                total += len(rec(x, y))
    return total


def part2(grid):
    m, n = len(grid), len(grid[0])

    def rec(x, y):
        if grid[x][y] == 9:
            return 1
        res = 0
        for nx, ny in neighbors4(x, y, m, n):
            if grid[nx][ny] == grid[x][y] + 1:
                res += rec(nx, ny)
        return res

    total = 0
    for x, row in enumerate(grid):
        for y, val in enumerate(row):
            if val == 0:
                total += rec(x, y)
    return total


test = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

data = get_and_write_data(10, 2024)
grid = parse(data)
print_output(part1(grid), part2(grid))
