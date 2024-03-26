from utils.data import *
import re


directions = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}


def parse(data):
    board, instructions = data.split("\n\n")
    board = [line.replace(" ", "x") for line in board.splitlines()]
    max_len = max(len(line) for line in board)
    board = list(map(lambda x: x.ljust(max_len, "x"), board))
    instructions = [int(instruction) if instruction.isdigit() else instruction for instruction in re.findall(r"\d+|[RL]", instructions)]
    return board, instructions


def find_boundaries(board):
    row_bounds = []
    for line in board:
        lfree, lwall, rfree, rwall = line.find("."), line.find("#"), line.rfind("."), line.rfind("#")
        left = min(lfree if lfree > -1 else float("inf"), lwall if lwall > -1 else float("inf"))
        right = max(rfree, rwall)
        row_bounds.append((left, right))
    col_bounds = []
    for line in map(lambda x: "".join(x), zip(*board)):
        lfree, lwall, rfree, rwall = line.find("."), line.find("#"), line.rfind("."), line.rfind("#")
        up = min(lfree if lfree > -1 else float("inf"), lwall if lwall > -1 else float("inf"))
        down = max(rfree, rwall)
        col_bounds.append((up, down))
    return row_bounds, col_bounds


def part1(board, instructions):
    row_bounds, col_bounds = find_boundaries(board)
    x = board[0].index(".")
    y = 0
    heading = 0
    for instruction in instructions:
        match instruction:
            case "R":
                heading = (heading + 1) % 4
            case "L":
                heading = (heading - 1) % 4
            case _:
                for _ in range(instruction):  # run steps
                    next_x = x + directions[heading][0]
                    next_y = y + directions[heading][1]
                    if heading in (0, 2):  # check if wrap around is needed
                        if next_x < row_bounds[next_y][0]:
                            next_x = row_bounds[next_y][1]
                        elif next_x > row_bounds[next_y][1]:
                            next_x = row_bounds[next_y][0]
                    else:
                        if next_y < col_bounds[next_x][0]:
                            next_y = col_bounds[next_x][1]
                        elif next_y > col_bounds[next_x][1]:
                            next_y = col_bounds[next_x][0]
                    if board[next_y][next_x] == "#":  # hit wall
                        break
                    x, y = next_x, next_y
    return 1000 * (y + 1) + 4 * (x + 1) + heading


def find_cubes(board, size):
    row_bounds, col_bounds = find_boundaries(board)
    width, height = len(board[0]), len(board)
    next_pos = [(0, row_bounds[0][0])]
    done = set()
    cubes = []
    while next_pos:
        y, x = next_pos.pop()
        done.add((y, x))
        if board[y][x] in ".#":
            cubes.append((x, x + size - 1, y, y + size - 1))  # left, right, upper, lower boundaries of cube (inclusive)
            for next_y, next_x in ((y, x + size), (y + size, x), (y, x - size), (y - size, x)):
                if (0 <= next_y < height and 0 <= next_x < width
                        and board[next_y][next_x] in ".#"
                        and (next_y, next_x) not in done):
                    next_pos.append((next_y, next_x))
    return cubes


def cube_transitions(board, size):  # no general solution for finding transitions between cube sides yet
    cubes = find_cubes(board, size)
    transitions = {0: {0: lambda x, y, cubes: (cubes[5][0], y, 0),
                       1: lambda x, y, cubes: (x, cubes[1][2], 1),
                       2: lambda x, y, cubes: (cubes[3][0], cubes[3][3] - (y % 50), 0),
                       3: lambda x, y, cubes: (cubes[4][0], cubes[4][2] + (x % 50), 0)},
                   1: {0: lambda x, y, cubes: (cubes[5][0] + (y % 50), cubes[5][3], 3),
                       1: lambda x, y, cubes: (x, cubes[2][2], 1),
                       2: lambda x, y, cubes: (cubes[3][0] + (y % 50), cubes[3][2], 1),
                       3: lambda x, y, cubes: (x, cubes[0][3], 3)},
                   2: {0: lambda x, y, cubes: (cubes[5][1], cubes[5][3] - (y % 50), 2),
                       1: lambda x, y, cubes: (cubes[4][1], cubes[4][2] + (x % 50), 2),
                       2: lambda x, y, cubes: (cubes[3][1], y, 2),
                       3: lambda x, y, cubes: (x, cubes[1][3], 3)},
                   3: {0: lambda x, y, cubes: (cubes[2][0], y, 0),
                       1: lambda x, y, cubes: (x, cubes[4][2], 1),
                       2: lambda x, y, cubes: (cubes[0][0], cubes[0][3] - (y % 50), 0),
                       3: lambda x, y, cubes: (cubes[1][0], cubes[1][2] + (x % 50), 0)},
                   4: {0: lambda x, y, cubes: (cubes[2][0] + (y % 50), cubes[2][3], 3),
                       1: lambda x, y, cubes: (cubes[5][0] + (x % 50), cubes[5][2], 1),
                       2: lambda x, y, cubes: (cubes[0][0] + (y % 50), cubes[0][2], 1),
                       3: lambda x, y, cubes: (x, cubes[3][3], 3)},
                   5: {0: lambda x, y, cubes: (cubes[2][1], cubes[2][3] - (y % 50), 2),
                       1: lambda x, y, cubes: (cubes[1][1], cubes[1][2] + (x % 50), 2),
                       2: lambda x, y, cubes: (cubes[0][1], y, 2),
                       3: lambda x, y, cubes: (cubes[4][0] + (x % 50), cubes[4][3], 3)}}
    return cubes, transitions


def find_cube_index(cubes, x, y):  # find which cube a given coordinate belongs to
    for i, (left, right, up, down) in enumerate(cubes):
        if left <= x <= right and up <= y <= down:
            return i


def part2(board, instructions):
    row_bounds, col_bounds = find_boundaries(board)
    cubes, transitions = cube_transitions(board, 50)
    x = board[0].index(".")
    y = 0
    heading = 0
    for i, instruction in enumerate(instructions):
        match instruction:
            case "R":
                heading = (heading + 1) % 4
            case "L":
                heading = (heading - 1) % 4
            case _:
                for _ in range(instruction):  # run steps
                    if ((x == row_bounds[y][0] and heading == 2) or (x == row_bounds[y][1] and heading == 0)
                       or (y == col_bounds[x][0] and heading == 3) or (y == col_bounds[x][1] and heading == 1)):
                        cube_idx = find_cube_index(cubes, x, y)
                        next_x, next_y, next_heading = transitions[cube_idx][heading](x, y, cubes)
                    else:
                        next_x = x + directions[heading][0]
                        next_y = y + directions[heading][1]
                        next_heading = heading
                    if board[next_y][next_x] == "#":  # hit wall
                        break
                    x, y, heading = next_x, next_y, next_heading
    return 1000 * (y + 1) + 4 * (x + 1) + heading


data = get_and_write_data(22, 2022)
board, instructions = parse(data)
print_output(part1(board, instructions), part2(board, instructions))