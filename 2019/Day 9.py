from utils.data import *
from utils.intcode import run


def parse(data):
    return list(map(int, data.split(",")))


def part1():
    prog = run(codes.copy())
    next(prog)
    return prog.send(1)


def part2():
    prog = run(codes.copy())
    next(prog)
    return prog.send(2)


test = """109, 1, 9, 2, 204, -6, 99"""

data = get_and_write_data(9, 2019)
codes = parse(data)
print_output(part1(), part2())
