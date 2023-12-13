from utils.data import *


def parse(data):
    return [list(map(int, row)) for row in data.splitlines()]


def get_visible(sequence):
    curr = -1
    visible = []
    for i, tree in enumerate(sequence):
        if tree > curr:
            visible.append(i)
            curr = tree
    return visible


def part1(trees):
    visible = set()
    n = len(trees) - 1
    for i, row in enumerate(trees):
        visible.update((i, t) for t in get_visible(row))
        visible.update((i, len(row) - 1 - t) for t in get_visible(reversed(row)))

    for j, col in enumerate(zip(*trees)):
        visible.update((t, j) for t in get_visible(col))
        visible.update((n - t, j) for t in get_visible(reversed(col)))

    return len(visible)


def scenic_score(trees, x, y):
    n = len(trees)
    m = len(trees[x])
    res = 1
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nx, ny = x + dx, y + dy
        cur = 0
        while 0 <= nx < n and 0 <= ny < m:
            cur += 1
            if trees[nx][ny] >= trees[x][y]:
                break
            nx += dx
            ny += dy
        res *= cur
    return res


def part2(trees):
    return max(scenic_score(trees, x, y) for x in range(len(trees)) for y in range(len(trees[x])))


data = get_and_write_data(8, 2022)
trees = parse(data)
print_output(part1(trees), part2(trees))
