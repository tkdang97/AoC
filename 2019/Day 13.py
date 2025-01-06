from utils.data import *
from utils.intcode import run


def parse(data):
    return list(map(int, data.split(",")))


def part1():
    tiles = {}
    program = run(codes.copy())
    while True:
        try:
            x = next(program)
            y = next(program)
            id = next(program)
            tiles[(x, y)] = id
        except StopIteration:
            break
    return sum(1 for val in tiles.values() if val == 2)


def part2():
    tiles = {}
    code = codes.copy()
    code[0] = 2
    program = run(code)
    score = 0
    ball_x = paddle_x = 0
    while True:
        try:
            x = next(program)
            if x is None:
                inp = -1 if ball_x < paddle_x else 1 if ball_x > paddle_x else 0
                x = program.send(inp)
            y = next(program)
            id = next(program)
            tiles[(x, y)] = id
            if id == 3:
                paddle_x = x
            if id == 4:
                ball_x = x
            if x == -1 and y == 0:
                score = id
        except StopIteration as e:
            print(e)
            break
    return score


test = """"""

data = get_and_write_data(13, 2019)
codes = parse(data)
print_output(part1(), part2())
