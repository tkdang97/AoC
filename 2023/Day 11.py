from utils.data import *
from bisect import bisect_left


def parse(data):
    res = data.splitlines()
    empty_rows = [i for i, row in enumerate(res) if "#" not in row]
    empty_cols = [i for i, col in enumerate(zip(*res)) if "#" not in col]
    coords = [(r, c) for r, row in enumerate(res) for c, val in enumerate(row) if val == "#"]
    return coords, empty_rows, empty_cols


def num_empty(p1, p2, empty):
    i1 = bisect_left(empty, p1)
    i2 = bisect_left(empty, p2)
    return abs(i1 - i2)


def shortest_path(point1, point2, empty_rows, empty_cols, factor):
    x1, y1 = point1
    x2, y2 = point2

    return (abs(x2 - x1) + (num_empty(x1, x2, empty_rows) * (factor - 1)) +
            abs(y2 - y1) + (num_empty(y1, y2, empty_cols) * (factor - 1)))


def solve(coords, empty_rows, empty_cols, factor):
    return sum(shortest_path(coords[i], coords[j], empty_rows, empty_cols, factor)
               for i in range(len(coords)) for j in range(i + 1, len(coords)))


data = get_and_write_data(11, 2023)
coords, empty_rows, empty_cols = parse(data)
print_output(solve(coords, empty_rows, empty_cols, 2), solve(coords, empty_rows, empty_cols, 1000000))
