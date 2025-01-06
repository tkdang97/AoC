from utils.data import *
from utils.grid import neighbors4
from collections import defaultdict
from itertools import combinations


def parse(data):
    return list(map(list, data.splitlines()))


def shortest_path(grid, start, end):
    m, n = len(grid), len(grid[0])
    seen = set()
    curr_level = [start]
    time = 0
    while curr_level:
        next_level = []
        for x, y in curr_level:
            if (x, y) == end:
                return time
            seen.add((x, y))
            for nx, ny in neighbors4(x, y, m, n):
                if grid[nx][ny] != "#" and (nx, ny) not in seen:
                    next_level.append((nx, ny))
                    seen.add((nx, ny))
        curr_level = next_level
        time += 1
    return -1


def get_distances(grid, start, end):
    m, n = len(grid), len(grid[0])
    distances_start = {start: 0}
    queue = [start]
    for x, y in queue:
        for next_pos in neighbors4(x, y, m, n):
            if next_pos not in distances_start and grid[next_pos[0]][next_pos[1]] != "#":
                distances_start[next_pos] = distances_start[(x, y)] + 1
                queue.append(next_pos)

    distances_end = {end: 0}
    queue = [end]
    for x, y in queue:
        for next_pos in neighbors4(x, y, m, n):
            if next_pos not in distances_end and grid[next_pos[0]][next_pos[1]] != "#":
                distances_end[next_pos] = distances_end[(x, y)] + 1
                queue.append(next_pos)

    return distances_start, distances_end


def solve(grid, max_duration):
    start = (0, 0)
    end = (0, 0)
    for x, row in enumerate(grid):
        for y, val in enumerate(row):
            if val == "S":
                start = (x, y)
            elif val == "E":
                end = (x, y)

    distances_start, distances_end = get_distances(grid, start, end)
    base = shortest_path(grid, start, end)
    count = 0
    for x, y in distances_start:
        for dx in range(-max_duration, max_duration + 1):
            max_y = max_duration - abs(dx)
            for dy in range(-max_y, max_y + 1):
                nx = x + dx
                ny = y + dy
                if (nx, ny) in distances_end:
                    manhattan = abs(x - nx) + abs(y - ny)
                    cheat_distance = distances_start[(x, y)] + distances_end[(nx, ny)] + manhattan
                    if base - cheat_distance >= 100:
                        count += 1
    return count


def part1(grid):
    return solve(grid, 2)


def part2(grid):
    return solve(grid, 20)


test = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

data = get_and_write_data(20, 2024)
grid = parse(data)
print_output(part1(grid), part2(grid))
