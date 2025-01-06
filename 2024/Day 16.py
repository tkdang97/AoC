from utils.data import *
from heapq import heappush, heappop


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse(data):
    grid = data.splitlines()
    start = (0, 0)
    end = (0, 0)
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == "S":
                start = (i, j)
            if val == "E":
                end = (i, j)
    return grid, start, end


def part1(grid, start, end):
    distances = {start: 0}
    m, n = len(grid), len(grid[0])
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    curr_x, curr_y = start
    dir_x, dir_y = 0, 1
    queue = []
    seen = set()
    heappush(queue, (0, start, (dir_x, dir_y)))
    while queue and (curr_x, curr_y) != end:
        dist, (curr_x, curr_y), (dir_x, dir_y) = heappop(queue)
        seen.add((curr_x, curr_y))
        for dx, dy in moves:
            if dx != -curr_x and dy != -curr_y:  # No use in turning 180 degrees and walking back
                nx, ny = curr_x + dx, curr_y + dy
                if (
                    0 <= nx < m and 0 <= ny < n and grid[nx][ny] != "#" and (nx, ny) not in seen
                ):  # check bounds and if it is a free square and not visited before
                    turn_cost = 1000 if dir_x != dx and dir_y != dy else 0
                    move_cost = turn_cost + 1
                    new_cost = move_cost + dist
                    if (nx, ny) not in distances or distances[(nx, ny)] > new_cost:
                        distances[(nx, ny)] = new_cost
                        heappush(queue, (new_cost, (nx, ny), (dx, dy)))
    return distances[end]


def generate_moves(grid, x, y, dir):
    yield 1000, (x, y, (dir - 1) % 4)
    yield 1000, (x, y, (dir + 1) % 4)
    dx, dy = directions[dir]
    nx, ny = x + dx, y + dy
    m, n = len(grid), len(grid[0])
    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] != "#":
        yield 1, (nx, ny, dir)
        
        
def part2(grid, start, end):
    distances = {start + (1,): 0}
    prev = {start + (1,): set()}
    curr_x, curr_y = start
    curr_dir = 1
    queue = []
    heappush(queue, (0, start, curr_dir))
    while queue:
        dist, (curr_x, curr_y), curr_dir = heappop(queue)
        for cost, (nx, ny, dir) in generate_moves(grid, curr_x, curr_y, curr_dir):
            new_cost = dist + cost
            if (nx, ny, dir) not in distances or distances[(nx, ny, dir)] > new_cost:
                distances[(nx, ny, dir)] = new_cost
                prev[(nx, ny, dir)] = {(curr_x, curr_y, curr_dir)}
                heappush(queue, (new_cost, (nx, ny), dir))
            elif distances[(nx, ny, dir)] == new_cost:
                prev[(nx, ny, dir)].add((curr_x, curr_y, curr_dir))
                
    best_end_keys = []
    best_end_val = float("inf")
    for (x, y, dir), dist in distances.items():
        if (x, y) == end:
            if dist < best_end_val:
                best_end_keys = [(x, y, dir)]
            elif dist == best_end_val:
                best_end_keys.append((x, y, dir))
    curr = best_end_keys
    squares = {end}
    while curr:
        nxt = curr.pop()
        squares.update({(x, y) for x, y, _ in prev[nxt]})
        curr.extend(prev[nxt])
    return len(squares)


test = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

data = get_and_write_data(16, 2024)
grid, start, end = parse(data)
print_output(part1(grid, start, end), part2(grid, start, end))
