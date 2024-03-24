from utils.data import *
import re
from tqdm import tqdm


def parse(data):
    res = []
    for x1, y1, x2, y2 in map(lambda x: map(int, x), re.findall(r"x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", data)):
        res.append(((x1, y1), abs(x1 - x2) + abs(y1 - y2)))
    return res


def part1(coords, target=2000000):
    found = set()
    for (x1, y1), dist in coords:
        if y1 - dist <= target <= y1 + dist:
            radius = dist - abs(y1 - target)
            for x in range(x1 - radius, x1 + radius + 1):
                found.add((x, target))
    return len(found - set(x[1] for x in coords))


def merge_intervals(intervals):
    if not intervals:
        return []
    sorted_intervals = sorted(intervals)
    res = [sorted_intervals[0]]
    for start, end in sorted_intervals[1:]:
        prev_start, prev_end = res[-1]
        if start <= prev_end:
            res.pop()
            res.append((prev_start, max(prev_end, end)))
    return res


def check_row(coords, y):
    blocked = []
    for (x1, y1), dist in coords:
        if y1 - dist <= y <= y1 + dist:
            r = dist - abs(y1 - y)
            blocked.append((x1 - r, x1 + r))
    for start, end in merge_intervals(blocked):
        if 0 < end < 4000000:
            return end + 1
    return None


def part2(coords, start=0, end=4000000):
    for y in tqdm(range(start, end + 1)):
        x = check_row(coords, y)
        if x:
            return x * 4000000 + y


data = get_and_write_data(15, 2022)
coords = parse(data)
print_output(part1(coords), part2(coords))
