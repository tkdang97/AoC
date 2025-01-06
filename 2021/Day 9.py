from utils.data import *
from utils.grid import neighbors4
from copy import deepcopy


def parse(data):
    field = [list(map(int, line)) for line in data.splitlines()]
    m, n = len(field), len(field[0])
    lows = []
    for x, row in enumerate(field):
        for y, val in enumerate(row):
            if all(field[nx][ny] > val for nx, ny in neighbors4(x, y, m, n)):
                lows.append((x, y))
    return field, lows


def part1(field, lows):
    return sum(field[x][y] + 1 for x, y in lows)


def part2(field, lows):
    tmp = deepcopy(field)
    m, n = len(field), len(field[0])
    sizes = []
    for lx, ly in lows:
        curr = [(lx, ly)]
        size = 0
        while curr:
            x, y = curr.pop()
            if tmp[x][y] != -1:
                size += 1
                tmp[x][y] = -1
                for nx, ny in neighbors4(x, y, m, n):
                    if tmp[nx][ny] not in (-1, 9):
                        curr.append((nx, ny))
        sizes.append(size)
    sizes.sort()
    return sizes[-1] * sizes[-2] * sizes[-3]


data = get_and_write_data(9, 2021)
parsed = parse(data)
print_output(part1(*parsed), part2(*parsed))