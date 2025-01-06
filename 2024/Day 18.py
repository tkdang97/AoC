from utils.data import *
from utils.grid import neighbors4
from heapq import heappush, heappop


def parse(data):
    return [tuple(map(int, line.split(","))) for line in data.splitlines()]


def bfs(coords, end_x, end_y, num_bytes):
    m, n = end_y + 1, end_x + 1
    seen = set(coords[:num_bytes])
    curr = {(0, 0)}
    step = 0
    while curr and (end_x, end_y) not in curr:
        nxt = set()
        for cx, cy in curr:
            seen.add((cx, cy))
            for next_coord in neighbors4(cx, cy, n, m):
                if next_coord not in seen:
                    nxt.add(next_coord)
        curr = nxt
        step += 1
    return step, (end_x, end_y) in curr


def part1(coords, end_x=70, end_y=70, num_bytes=1024):
    return bfs(coords, end_x, end_y, num_bytes)[0]


def part2(coords, end_x=70, end_y=70, start=1024):
    left = start
    right = len(coords)
    while left < right:
        mid = (left + right) // 2
        _, found = bfs(coords, end_x, end_y, mid)
        if found:
            left = mid + 1
        else:
            right = mid
    return ",".join(map(str, coords[left - 1]))


test = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

data = get_and_write_data(18, 2024)
coords = parse(data)
print_output(part1(coords), part2(coords))
