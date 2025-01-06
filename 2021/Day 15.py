from utils.data import *
from utils.grid import neighbors4
import heapq


def parse(data):
    return [list(map(int, line)) for line in data.splitlines()]


def solve(risks):
    max_x, max_y = len(risks), len(risks[0])
    tmp = [[float("inf")] * max_y for _ in range(max_x)]
    tmp[0][0] = 0
    q = [(tmp[x][y], x, y) for x in range(len(tmp)) for y in range(len(tmp[x]))]
    while q:
        dist, x, y = heapq.heappop(q)
        if (x, y) == (max_x - 1, max_y - 1):
            break
        for nx, ny in neighbors4(x, y, max_x, max_y):
            new_dist = dist + risks[nx][ny]
            if new_dist < tmp[nx][ny]:
                tmp[nx][ny] = new_dist
                heapq.heappush(q, (new_dist, nx, ny))
    return tmp[max_x - 1][max_y - 1]


def part1(risks):
    return solve(risks)


def part2(risks):
    m, n = len(risks), len(risks[0])
    full_risks = [[0] * (5 * m) for _ in range(5 * n)]
    for x, row in enumerate(risks):
        for y, val in enumerate(row):
            for dx in range(5):
                for dy in range(5):
                    full_risks[x + dx * m][y + dy * n] = (val + dx + dy - 1) % 9 + 1

    return solve(full_risks)


data = get_and_write_data(15, 2021)
risks = parse(data)
print_output(part1(risks), part2(risks))
