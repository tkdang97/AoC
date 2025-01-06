from utils.data import *
from collections import deque
import heapq


def parse(data):
    return data.splitlines()


def bfs(grid, key, start_pos, paths):
    paths[key] = {}
    num_steps = 0
    curr = [(start_pos, set())]
    seen = {start_pos}
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
    while curr:
        nxt = []
        for (x, y), doors in curr:
            val = grid[x][y]
            next_doors = doors.copy()
            if val.isalpha() and val.islower() and val != key:
                paths[key][val] = (num_steps, doors.copy())
            elif val.isalpha() and val.isupper():  # door
                next_doors |= {val.lower()}  # add required key
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in seen and grid[nx][ny] != "#":
                    nxt.append(((nx, ny), next_doors.copy()))
                    seen.add((nx, ny))
        curr = nxt
        num_steps += 1


def get_paths(grid):
    positions = {}
    robot_pos = None
    for x, row in enumerate(grid):
        for y, val in enumerate(row):
            if val == "@":
                robot_pos = (x, y)
            elif val.isalpha() and val.islower():
                positions[val] = (x, y)

    key_paths = {}
    bfs(grid, "@", robot_pos, key_paths)
    for key, pos in positions.items():
        bfs(grid, key, pos, key_paths)
    return key_paths


def dijkstra(grid, part2=False):
    paths = get_paths(grid)
    keys = set(paths.keys())
    curr = [(0, "@", {"@"})]
    distances = {}
    while curr:
        dist, key, collected = heapq.heappop(curr)
        if collected == keys:
            return dist
        for candidate, (cdist, doors) in paths[key].items():
            if candidate not in collected and (part2 or doors.issubset(collected)):
                dist_key = (candidate, tuple(sorted(collected | {candidate})))
                if dist_key not in distances or distances[dist_key] > dist + cdist:
                    heapq.heappush(curr, (dist + cdist, candidate, collected | {candidate}))
                    distances[dist_key] = dist + cdist
    return None


def part1():
    return dijkstra(grid)


def part2():
    mid_x = len(grid) // 2
    mid_y = len(grid[0]) // 2
    modified_grid = grid.copy()
    modified_grid[mid_x - 1] = modified_grid[mid_x - 1][: mid_y - 1] + "@#@" + modified_grid[mid_x - 1][mid_y + 2 :]
    modified_grid[mid_x] = modified_grid[mid_x][: mid_y - 1] + "###" + modified_grid[mid_x][mid_y + 2 :]
    modified_grid[mid_x + 1] = modified_grid[mid_x + 1][: mid_y - 1] + "@#@" + modified_grid[mid_x + 1][mid_y + 2 :]
    grids = (
        [row[: mid_y + 1] for row in modified_grid[: mid_x + 1]],
        [row[mid_y:] for row in modified_grid[: mid_x + 1]],
        [row[: mid_y + 1] for row in modified_grid[mid_x:]],
        [row[mid_y:] for row in modified_grid[mid_x:]],
    )
    return sum(dijkstra(sub, True) for sub in grids)


data = get_and_write_data(18, 2019)
grid = parse(data)
print_output(part1(), part2())
