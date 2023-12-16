from utils.data import *


# direction changes in order: up, right, down, left
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


def parse(data):
    return data.splitlines()


def move(row, column, direction):
    global dr, dc
    return row + dr[direction], column + dc[direction], direction


def in_bounds(row, col, row_lim, col_lim):
    return 0 <= row < row_lim and 0 <= col < col_lim


def solve(grid, start_row, start_col, start_direction):
    positions = [(start_row, start_col, start_direction)]
    seen = set()
    n = len(grid)
    m = len(grid[0])
    while positions:
        next_positions = []
        for row, col, direction in positions:
            if (row, col, direction) not in seen and in_bounds(row, col, n, m):
                seen.add((row, col, direction))
                curr = grid[row][col]
                if curr == ".":
                    next_positions.append(move(row, col, direction))
                elif curr == "/":
                    next_positions.append(move(row, col, {0: 1, 1: 0, 2: 3, 3: 2}[direction]))
                elif curr == "\\":
                    next_positions.append(move(row, col, {0: 3, 1: 2, 2: 1, 3: 0}[direction]))
                elif curr == "|":
                    if direction in (0, 2):
                        next_positions.append(move(row, col, direction))
                    else:
                        next_positions.extend((move(row, col, 0), move(row, col, 2)))
                else:
                    if direction in (1, 3):
                        next_positions.append(move(row, col, direction))
                    else:
                        next_positions.extend((move(row, col, 1), move(row, col, 3)))
        positions = next_positions
    return len(set([(x[0], x[1]) for x in seen]))


def part1(grid):
    return solve(grid, 0, 0, 1)


def part2(grid):
    res = 0
    n = len(grid)
    m = len(grid[0])
    for r in range(n):
        res = max(res, solve(grid, r, 0, 1), solve(grid, r, m - 1, 3))
    for c in range(m):
        res = max(res, solve(grid, 0, c, 2), solve(grid, n - 1, c, 0))
    return res


data = get_and_write_data(16, 2023)
grid = parse(data)
print_output(part1(grid), part2(grid))
