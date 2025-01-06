from utils.data import *
from collections import defaultdict


def parse(data):
    return data.splitlines()


def search_position(grid, row, col, word):
    if grid[row][col] != word[0]:
        return 0, []
    m, n = len(grid), len(grid[0])
    directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    res = 0
    dirs = []
    for dr, dc in directions:
        curr_row, curr_col = row + dr, col + dc
        for i in range(1, len(word)):
            if curr_row >= m or curr_row < 0 or curr_col >= n or curr_col < 0 or grid[curr_row][curr_col] != word[i]:
                break

            curr_row += dr
            curr_col += dc
        else:
            res += 1
            dirs.append((dr, dc))
    return res, dirs


def part1(grid):
    total = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            total += search_position(grid, row, col, "XMAS")[0]
    return total


def part2(grid):
    found = defaultdict(list)
    diagonals = {
        (1, 1): [((2, 0), (-1, 1)), ((0, 2), (1, -1))],
        (1, -1): [((2, 0), (-1, -1))],
        (-1, 1): [((0, 2), (-1, -1))],
        (-1, -1): [],
    }
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            _, dirs = search_position(grid, row, col, "MAS")
            for direction in dirs:
                if direction in diagonals:
                    found[(row, col)].append(direction)

    total = 0
    for (row, col), directions in found.items():
        for direction in directions:
            for instruction in diagonals[direction]:
                (dr, dc), direction = instruction
                nr, nc = row + dr, col + dc
                if (nr, nc) in found and direction in found[(nr, nc)]:
                    total += 1
    return total


test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

data = get_and_write_data(4, 2024)
grid = parse(data)
print_output(part1(grid), part2(grid))
