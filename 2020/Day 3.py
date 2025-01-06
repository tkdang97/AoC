from utils.data import *


def parse(data):
    return data.splitlines()


def count_trees(grid, dx, dy):
    m, n = len(grid), len(grid[0])
    x, y = 0, 0
    res = 0
    while x < m:
        if grid[x][y] == "#":
            res += 1
        x += dx
        y = (y + dy) % n
    return res


def part1(grid):
    return count_trees(grid, 1, 3)


def part2(grid):
    slopes = ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))
    res = 1
    for dx, dy in slopes:
        res *= count_trees(grid, dx, dy)
    return res


test = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""

data = get_and_write_data(3, 2020)
grid = parse(data)
print_output(part1(grid), part2(grid))
