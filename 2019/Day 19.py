from utils.data import *
from utils.intcode import run
from itertools import count


def parse(data):
    return list(map(int, data.split(",")))


def check(x, y):
    program = run(codes.copy())
    next(program)
    program.send(x)
    return program.send(y)


def part1():
    return sum(check(x, y) for x in range(50) for y in range(50))


def part2():
    x = 0
    for y in count(start=99):
        while not check(x, y):
            x += 1
        if check(x + 99, y - 99):
            return 10000 * x + (y - 99)
        

data = get_and_write_data(19, 2019)
codes = parse(data)
print_output(part1(), part2())
