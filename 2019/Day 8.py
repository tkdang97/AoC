from utils.data import *
from collections import Counter


def parse(data):
    return list(map(int, data))


def part1():
    min_zero_count = len(pixels)
    res = 0
    layer_length = width * height
    for i in range(0, len(pixels), layer_length):
        counts = Counter(pixels[i : i + layer_length])
        if counts[0] < min_zero_count:
            min_zero_count = counts[0]
            res = counts[1] * counts[2]
    return res


def part2():
    positions = [[[] for _ in range(width)] for _ in range(height)]
    layer_length = width * height
    for i, val in enumerate(pixels):
        relative = i % layer_length
        x, y = relative // width, relative % width
        positions[x][y].append(val)
    res = []
    for row in positions:
        row_data = []
        for pos in row:
            row_data.append(next(str(val) for val in pos if val != 2))
        res.append(row_data)
    print("\n".join("".join(row).replace("0", " ").replace("1", "#") for row in res))


test = """0222112222120000"""

data = get_and_write_data(8, 2019)
pixels = parse(data)
width, height = 25, 6
print_output(part1(), part2())
