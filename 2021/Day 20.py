from utils.data import *


def parse(data: str) -> tuple[str, set[tuple[int, int]]]:
    algo, image = data.split("\n\n")
    algo = algo.replace("\n", "")
    points = set()
    for x, line in enumerate(image.splitlines()):
        for y, symbol in enumerate(line):
            if symbol == "#":
                points.add((x, y))
    return algo, points


def calculate_output(x: int, y: int, image: set[tuple[int, int]], fill: str, min_x, max_x, min_y, max_y) -> int:
    res = ""
    for dx in (x - 1, x, x + 1):
        for dy in (y - 1, y, y + 1):
            if dx < min_x or dx > max_x or dy < min_y or dy > max_y:
                res += fill
            else:
                res += ("1" if (dx, dy) in image else "0")
    return int(res, 2)


def run_step(image: set[tuple[int, int]], algo: str, step: int) -> set[tuple[int, int]]:
    min_x, min_y = map(min, zip(*image))
    max_x, max_y = map(max, zip(*image))
    output = set()
    fill_value = "1" if algo[0] == "#" and step % 2 else "0"
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            if algo[calculate_output(x, y, image, fill_value, min_x - (step == 0),
                                     max_x + (step == 0), min_y - (step == 0), max_y + (step == 0))] == "#":
                output.add((x, y))
    return output


def part1(algo: str, image: set[tuple[int, int]]) -> int:
    out = image
    for i in range(2):
        out = run_step(out, algo, i)
    return len(out)


def part2(algo: str, image: set[tuple[int, int]]) -> int:
    out = image
    for i in range(50):
        out = run_step(out, algo, i)
    return len(out)


data = get_and_write_data(20, 2021)
parsed = parse(data)
print_output(part1(*parsed), part2(*parsed))
