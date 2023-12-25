from utils.data import *
from utils.grid import neighbors4
from collections import defaultdict


def parse(data):
    res = data.splitlines()
    start = (0, res[0].index("."))
    end = (len(res) - 1, res[-1].index("."))
    return res, start, end


@timeit
def part1(grid, start, end):
    DIRS = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
    n, m = len(grid), len(grid[0])
    queue = [start + (0, )]
    seen = set()
    res = 0
    while queue:
        row, col, dist = queue.pop()
        if dist == -1:
            seen.remove((row, col))
            continue
        if (row, col) == end:
            res = max(res, dist)
            continue
        if (row, col) in seen:
            continue
        seen.add((row, col))

        # Add current point with distance -1 as an "anchor point" to be able to remove it from the visited set later on
        # This is needed so that a different path can still visit this coordinate again
        queue.append((row, col, -1))
        if grid[row][col] in DIRS:
            dr, dc = DIRS[grid[row][col]]
            queue.append((row + dr, col + dc, dist + 1))
        else:
            for nr, nc in neighbors4(row, col, n, m):
                if grid[nr][nc] != "#":
                    queue.append((nr, nc, dist + 1))
    return res


def build_edges(grid):
    n, m = len(grid), len(grid[0])
    edges = defaultdict(set)
    for r, row in enumerate(grid):
        for c, sym in enumerate(row):
            if sym != "#":
                for nr, nc in neighbors4(r, c, n, m):
                    if grid[nr][nc] != "#":
                        edges[(r, c)].add((nr, nc, 1))

    # merging edges for nodes with degree two, because that means the node lies between two other nodes
    # which can instead directly be connected with a longer edge
    while True:
        for (row, col), edge_set in edges.items():
            if len(edge_set) == 2:
                (nr1, ncol1, dist1), (nr2, ncol2, dist2) = edge_set
                edges[(nr1, ncol1)].remove((row, col, dist1))
                edges[(nr2, ncol2)].remove((row, col, dist2))
                edges[(nr1, ncol1)].add((nr2, ncol2, dist1 + dist2))
                edges[(nr2, ncol2)].add((nr1, ncol1, dist1 + dist2))
                del edges[(row, col)]
                break
        else:
            break
    return edges


@timeit
def part2(grid, start, end):
    edges = build_edges(grid)
    queue = [start + (0, )]
    seen = set()
    res = 0
    while queue:
        row, col, dist = queue.pop()
        if dist == -1:
            seen.remove((row, col))
            continue
        if (row, col) == end:
            res = max(res, dist)
            continue
        if (row, col) in seen:
            continue
        seen.add((row, col))
        queue.append((row, col, -1))
        for nr, ncol, next_dist in edges[(row, col)]:
            queue.append((nr, ncol, dist + next_dist))
    return res


data = get_and_write_data(23, 2023)
grid, start, end = parse(data)
print_output(part1(grid, start, end), part2(grid, start, end))
