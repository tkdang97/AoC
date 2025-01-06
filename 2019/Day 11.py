from utils.data import *
from utils.intcode import run


def parse(data):
    return list(map(int, data.split(",")))
            
            
def paint(part2=False):
    dirs = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    x = y = 0
    white = {(0, 0)} if part2 else set()
    black = set()
    curr_dir = 0
    program = run(codes.copy())
    while True:
        try:
            next(program)
            inp = 1 if (x, y) in white else 0
            color = program.send(inp)
            turn = next(program)
            if color == 0:
                black.add((x, y))
                white.discard((x, y))
            else:
                white.add((x, y))
                black.discard((x, y))
            dir = -1 if turn == 0 else 1
            curr_dir = (curr_dir + dir) % 4
            dx, dy = dirs[curr_dir]
            x, y = x + dx, y + dy
        except StopIteration as e:
            break
    return white, black


def part1():
    return len(set.union(*paint()))


def part2():
    white, black = paint(True)
    combined = white | black
    min_x, max_x = min(c[0] for c in combined), max(c[0] for c in combined)
    min_y, max_y = min(c[1] for c in combined), max(c[1] for c in combined)
    width, height = max_y - min_y + 1, max_x - min_x + 1
    grid = [[" "] * width for _ in range(height)]
    for x, y in white:
        grid[x][y] = "#"
    print("\n".join("".join(row) for row in grid))


test = """"""

data = get_and_write_data(11, 2019)
codes = parse(data)
print_output(part1(), part2())
