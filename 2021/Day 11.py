from utils.data import *
from utils.grid import neighbors8
from copy import deepcopy
from itertools import count


def parse(data):
    return [list(map(int, line)) for line in data.splitlines()]


def flash(energies, x, y, marked):
    marked.add((x, y))
    for nx, ny in neighbors8(x, y, len(energies), len(energies[0])):
        if (nx, ny) not in marked:
            energies[nx][ny] += 1
            if energies[nx][ny] > 9:
                flash(energies, nx, ny, marked)
    energies[x][y] = 0


def part1(energies):
    tmp = deepcopy(energies)
    total = 0
    for i in range(100):
        marked = set()
        for x, row in enumerate(tmp):
            for y in range(len(row)):
                if (x, y) not in marked:
                    tmp[x][y] += 1
                    if tmp[x][y] > 9:
                        flash(tmp, x, y, marked)
        total += len(marked)
    return total


def part2(energies):
    tmp = deepcopy(energies)
    for i in count(1):
        marked = set()
        for x, row in enumerate(tmp):
            for y in range(len(row)):
                if (x, y) not in marked:
                    tmp[x][y] += 1
                    if tmp[x][y] > 9:
                        flash(tmp, x, y, marked)
        if len(marked) == 100:
            return i
        assert i < 100000


data = get_and_write_data(11, 2021)
energies = parse(data)
print_output(part1(energies), part2(energies))