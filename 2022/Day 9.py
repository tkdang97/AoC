from utils.data import *
from itertools import pairwise


MOVES = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}


def parse(data):
    res = []
    for line in data.splitlines():
        move, count = line.split()
        res.append((move, int(count)))
    return res


def update_coords(px, py, cx, cy):
    diff_x = cx - px
    diff_y = cy - py
    if diff_x == 0 or diff_y == 0:
        if abs(diff_x) >= 2:
            cx -= 1 if diff_x > 0 else -1
        if abs(diff_y) >= 2:
            cy -= 1 if diff_y > 0 else -1
    elif (abs(diff_x), abs(diff_y)) != (1, 1):
        cx -= 1 if diff_x > 0 else -1
        cy -= 1 if diff_y > 0 else -1
    return cx, cy


def part1(steps):
    head = (0, 0)
    tail = (0, 0)
    visited = {(0, 0)}
    for move, count in steps:
        hx, hy = head
        tx, ty = tail
        dx, dy = MOVES[move]
        for _ in range(count):
            hx += dx
            hy += dy
            tx, ty = update_coords(hx, hy, tx, ty)
            visited.add((tx, ty))
        head = (hx, hy)
        tail = (tx, ty)
    return len(visited)


def part2(steps, num_knots=10):
    knots = [(0, 0) for _ in range(num_knots)]
    visited = set()
    for move, count in steps:
        dx, dy = MOVES[move]
        visited.add(knots[-1])
        for _ in range(count):
            knots[0] = (knots[0][0] + dx, knots[0][1] + dy)
            for i in range(1, num_knots):
                px, py = knots[i - 1]
                cx, cy = knots[i]
                knots[i] = update_coords(px, py, cx, cy)
            visited.add(knots[-1])
    return len(visited)


data = get_and_write_data(9, 2022)
steps = parse(data)
print_output(part1(steps), part2(steps))
