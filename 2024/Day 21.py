from utils.data import *
from functools import cache
from collections import deque


def parse(data):
    return data.splitlines()


@cache
def best_dirpad(x, y, dx, dy, robots, invalid):
    ret = None
    todo = deque([(x, y, "")])

    while len(todo) > 0:
        x, y, path = todo.popleft()
        if (x, y) == (dx, dy):
            ret = minn(ret, best_robot(path + "A", robots - 1))
        elif (x, y) != invalid:
            for ox, oy, val in ((-1, 0, "<"), (1, 0, ">"), (0, -1, "^"), (0, 1, "v")):
                if is_dir(x, dx, ox) or is_dir(y, dy, oy):
                    todo.append((x + ox, y + oy, path + val))

    return ret


@cache
def best_robot(path, robots):
    if robots == 1:
        return len(path)

    ret = 0
    pad = decode_pad(".^A<v>", 3)
    x, y = pad["A"]

    for val in path:
        dx, dy = pad[val]
        ret += best_dirpad(x, y, dx, dy, robots, pad["."])
        x, y = dx, dy

    return ret


def minn(*vals):
    vals = [x for x in vals if x is not None]
    return min(vals)


def decode_pad(val, width):
    return {val: (x % width, x // width) for x, val in enumerate(val)}


def is_dir(start, dest, change):
    return (change < 0 and dest < start) or (change > 0 and dest > start)


def solve(values, mode):
    ret = 0
    pad = decode_pad("789456123.0A", 3)
    for row in values:
        result = 0
        x, y = pad["A"]
        for val in row:
            dx, dy = pad[val]
            result += best_dirpad(x, y, dx, dy, 4 if mode == 1 else 27, pad["."])
            x, y = dx, dy
        ret += result * int(row[:-1].lstrip("0"))
    return ret


def part1(codes):
    return solve(codes, 1)


def part2(codes):
    return solve(codes, 2)


test = """029A
980A
179A
456A
379A
"""

data = get_and_write_data(21, 2024)
codes = parse(data)
print_output(part1(codes), part2(codes))
