from utils.data import *
from utils.grid import *
from itertools import count


def parse(data):
    res = list(map(list, data.splitlines()))
    start = (0, 0)
    for i, row in enumerate(res):
        for j, val in enumerate(row):
            if val == "S":
                start = (i, j)
                res[i][j] = "."
    return res, start


def part1(grid, start, num_steps):
    n = len(grid)
    m = len(grid[0])
    positions = {start}
    for _ in range(num_steps):
        new_positions = set()
        for row, col in positions:
            for new_row, new_col in neighbors4(row, col, n, m):
                if grid[new_row][new_col] == ".":
                    new_positions.add((new_row, new_col))
        positions = new_positions
    return len(positions)


# interpolation formula from https://www2.lawrence.edu/fast/GREGGJ/CMSC210/arithmetic/interpolation.html
def quadratic(y0, y1, y2, x):
    diff1 = y1 - y0
    diff2 = y2 - y1
    c = y0
    b = diff1
    a = (diff2 - diff1) // 2
    return a * (x - 1) * x + b * x + c


def part2(grid, start):
    n = len(grid)
    m = len(grid[0])
    positions = {start}
    ys = []
    target = 26501365
    for i in count(1):
        if len(ys) >= 3:
            break
        new_positions = set()
        for row, col in positions:
            for new_row, new_col in ((row - 1, col), (row, col - 1), (row + 1, col), (row, col + 1)):
                if grid[new_row % n][new_col % m] == ".":
                    new_positions.add((new_row, new_col))
        positions = new_positions
        if i % n == target % n:
            ys.append(len(positions))
    return quadratic(*ys, target // n)


data = get_and_write_data(21, 2023)
grid, start = parse(data)
print_output(part1(grid, start, 64), part2(grid, start))
