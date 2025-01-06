from utils.data import *

directions = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}


def parse(data):
    grid = [list(line) for line in data.splitlines()]
    guard_position = next((i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == "^")
    return grid, guard_position


def part1(grid, guard_pos):
    m, n = len(grid), len(grid[0])
    curr_dir = 0
    curr_x, curr_y = guard_pos
    seen = set()
    while True:
        key = (curr_x, curr_y, curr_dir)
        dx, dy = directions[curr_dir]
        next_x, next_y = curr_x + dx, curr_y + dy
        if key in seen:
            break
        seen.add(key)
        if next_x < 0 or next_x >= m or next_y < 0 or next_y >= n:
            break
        if grid[next_x][next_y] == "#":
            curr_dir = (curr_dir + 1) % 4
        else:
            curr_x, curr_y = next_x, next_y

    visited = set((x, y) for x, y, _ in seen)
    return visited


def part2(grid, guard_pos):
    positions = part1(grid, guard_pos)
    m, n = len(grid), len(grid[0])
    res = 0
    for i, j in positions:
        if grid[i][j] == ".":
            grid[i][j] = "#"
            curr_dir = 0
            curr_x, curr_y = guard_pos
            seen = set()
            while True:
                key = (curr_x, curr_y, curr_dir)
                dx, dy = directions[curr_dir]
                next_x, next_y = curr_x + dx, curr_y + dy
                if key in seen:
                    res += 1
                    break
                seen.add(key)
                if next_x < 0 or next_x >= m or next_y < 0 or next_y >= n:
                    break
                if grid[next_x][next_y] == "#":
                    curr_dir = (curr_dir + 1) % 4
                else:
                    curr_x, curr_y = next_x, next_y
            grid[i][j] = "."
    return res


test = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

data = get_and_write_data(6, 2024)
grid, guard_pos = parse(data)
print_output(len(part1(grid, guard_pos)), part2(grid, guard_pos))
