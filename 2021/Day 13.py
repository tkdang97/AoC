from utils.data import *
from copy import deepcopy
import re


def parse(data):
    positions = {(int(x), int(y)) for x, y in re.findall(r"(\d+),(\d+)", data)}
    instructions = [(ax, int(line)) for ax, line in re.findall(r"fold along (\w+)=(\d+)", data)]
    return positions, instructions


def fold(positions, instruction):
    comp_idx = 0 if instruction[0] == "x" else 1
    line = instruction[1]
    new_pos = set()
    for pos in positions:
        if pos[comp_idx] > line:
            if comp_idx == 0:
                new_pos.add((line - abs(line - pos[0]), pos[1]))
            else:
                new_pos.add((pos[0], line - abs(line - pos[1])))
        else:
            new_pos.add(pos)
    return new_pos


def part1(positions, instructions):
    return len(fold(positions, instructions[0]))


def part2(positions, instructions):
    new_pos = deepcopy(positions)
    for inst in instructions:
        new_pos = fold(new_pos, inst)
    max_x, max_y = map(max, zip(*new_pos))
    min_x, min_y = map(min, zip(*new_pos))
    board = [["."] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for x, y in new_pos:
        board[y + min_y][x + min_x] = "#"
    print("\n".join("".join(line) for line in board))


test = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

data = get_and_write_data(13, 2021)
parsed = parse(data)
print_output(part1(*parsed), part2(*parsed))
