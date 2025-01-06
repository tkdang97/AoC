from utils.data import *
from utils.intcode import run
from itertools import combinations


def parse(data):
    return list(map(int, data.split(",")))


def part1():
    program = run(codes.copy())
    s = ""
    while True:
        try:
            s += chr(next(program))
        except StopIteration:
            break
    lines = s.splitlines()
    scaffoldings = {(x, y) for x, row in enumerate(lines) for y, val in enumerate(row) if val != "."}
    res = 0
    for x, y in scaffoldings:
        if (
            (x - 1, y) in scaffoldings
            and (x + 1, y) in scaffoldings
            and (x, y - 1) in scaffoldings
            and (x, y + 1) in scaffoldings
        ):
            res += x * y
    robot_pos = next((x, y) for x, y in scaffoldings if lines[x][y] in "^>v<")
    return res, scaffoldings, robot_pos, "^>v<".index(lines[robot_pos[0]][robot_pos[1]])


def can_generate(lst, sublists):
    n = len(lst)
    i = 0
    order = []
    while i < n:
        matched = False
        for j, sub in enumerate(sublists):
            if lst[i : i + len(sub)] == sub:
                i += len(sub)
                matched = True
                order.append(j)
                break
        if not matched:
            return False, []
    return True, order


def find_sublists(lst):
    n = len(lst)
    joined = [lst[i] + lst[i + 1] for i in range(0, len(lst) - 1, 2)]  # join turns and steps to reduce combinations
    possible_sublists = []

    # Generate all possible sublists of maximum length 5
    for i in range(n):
        for j in range(i + 1, min(n + 1, i + 6)):
            sub = joined[i:j]
            if sub and sub not in possible_sublists:
                possible_sublists.append(sub)

    for subs in combinations(possible_sublists, 3):
        possible, order = can_generate(joined, subs)
        if possible:
            return [
                [part for instr in sub for part in (instr[0], instr[1:])] for sub in subs
            ], order  # split the result back up in single chars

    return None, []  # If no valid decomposition found


def find_path():
    dirs = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    curr_dir = robot_dir
    num_steps = 0
    visited = set()
    curr_x, curr_y = start
    instructions = []
    while len(visited) < len(scaffoldings):
        visited.add((curr_x, curr_y))
        dx, dy = dirs[curr_dir]
        nx, ny = curr_x + dx, curr_y + dy
        if (nx, ny) not in scaffoldings:  # need to turn
            if num_steps:
                instructions.append(str(num_steps))
            num_steps = 0
            test_dir = (curr_dir - 1) % 4  # try left
            left_x, left_y = curr_x + dirs[test_dir][0], curr_y + dirs[test_dir][1]
            if (left_x, left_y) in scaffoldings:
                instructions.append("L")
            else:
                test_dir = (curr_dir + 1) % 4
                instructions.append("R")
            curr_dir = test_dir
        else:
            curr_x, curr_y = nx, ny
            num_steps += 1
    return find_sublists(instructions)


def part2():
    code = codes.copy()
    code[0] = 2
    program = run(code)
    sublists, order = find_path()
    main_str = ",".join(chr(ord("A") + i) for i in order)
    program_str = "\n".join([main_str] + [",".join(sub) for sub in sublists]) + "\nn\n"
    while True:
        try:
            out = next(program)
        except StopIteration:
            break
        while isinstance(out, str) and out == "input":
            out = program.send(ord(program_str[0]))
            program_str = program_str[1:]
    return out


test = """"""

data = get_and_write_data(17, 2019)
codes = parse(data)
p1, scaffoldings, start, robot_dir = part1()
find_path()
print_output(p1, part2())
