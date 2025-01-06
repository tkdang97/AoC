from utils.data import *
from utils.intcode import run


DIRS = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}


def parse(data):
    return list(map(int, data.split(",")))


def replay(program, moves, reverse=False):
    if moves:
        steps = moves if not reverse else [move + 1 if move % 2 == 1 else move - 1 for move in reversed(moves)]
        for step in steps:
            next(program)
            assert program.send(step) != 0


def part1():
    program = run(codes.copy())
    curr = [((0, 0), [])]
    seen = {(0, 0)}
    num_steps = 0
    walls = set()
    res = None
    coords = None
    while curr:
        nxt = []
        for (x, y), moves in curr:
            replay(program, moves)  # walk to position
            for dir, (dx, dy) in DIRS.items():
                nx, ny = x + dx, y + dy
                if (nx, ny) not in seen:
                    seen.add((nx, ny))
                    next(program)
                    code = program.send(dir)
                    if code == 0:  # hit wall, no need to explore there
                        walls.add((nx, ny))
                    elif (
                        code == 1
                    ):  # moved forward into free location, explore in next iteration, move back one space for now
                        nxt.append(((nx, ny), moves + [dir]))
                        replay(program, [dir], True)
                    elif code == 2:  # found oxygen system
                        nxt.append(((nx, ny), moves + [dir]))
                        replay(program, [dir], True)
                        res = num_steps + 1
                        coords = (nx, ny)
            replay(program, moves, True)  # walk back to start
        curr = nxt
        num_steps += 1
    return res, walls, coords


def part2():
    seen = {oxygen_coords}
    curr = {oxygen_coords}
    num_steps = 0
    while curr:
        nxt = []
        for x, y in curr:
            for (dx, dy) in DIRS.values():
                nx, ny = x + dx, y + dy
                if (nx, ny) not in seen and (nx, ny) not in walls:
                    nxt.append((nx, ny))
                    seen.add((nx, ny))
        curr = nxt
        num_steps += 1
    return num_steps - 1            


test = """"""

data = get_and_write_data(15, 2019)
codes = parse(data)
p1, walls, oxygen_coords = part1()
print_output(p1, part2())
