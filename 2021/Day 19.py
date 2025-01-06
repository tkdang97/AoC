from utils.data import *
import re
import itertools
from collections import Counter

# from https://www.reddit.com/r/adventofcode/comments/rjpf7f/comment/hp78lpo/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

vectors = list[tuple[int, int, int]]


def parse(data: str) -> list[vectors]:
    scanners = data.split("\n\n")
    beacons = []
    for scanner in scanners:
        beacons.append([tuple(map(int, beacon)) for beacon in re.findall(r"(-?\d+),(-?\d+),(-?\d+)", scanner)])
    return beacons


def try_align(aligned: vectors, candidate: list[vectors]) -> tuple[vectors, list[int, int, int]] | None:
    ret = []
    dl = []
    dp = dpp = None
    for dim in range(3):
        x = [pos[dim] for pos in aligned]
        for (d, s) in [(0, 1), (1, 1), (2, 1), (0, -1), (1, -1), (2, -1)]:
            if d == dp or d == dpp:
                continue
            t = [pos[d] * s for pos in candidate]
            w = [b - a for (a, b) in itertools.product(x, t)]
            c = Counter(w).most_common(1)
            if c[0][1] >= 12:
                break
        if c[0][1] < 12:
            return None
        (dpp, dp) = (dp, d)
        ret.append([v - c[0][0] for v in t])
        dl.append(c[0][0])
    return list(zip(ret[0], ret[1], ret[2])), dl


def part1(beacons: list[vectors]) -> int:
    done = set()
    next = [beacons[0]]
    rest = beacons[1:]
    while next:
        aligned = next.pop()
        tmp = []
        for candidate in rest:
            r = try_align(aligned, candidate)
            if r:
                (updated, shift) = r
                next.append(updated)
            else:
                tmp.append(candidate)
        rest = tmp
        done.update(aligned)
    return len(done)


def part2(beacons: list[vectors]) -> int:
    next = [beacons[0]]
    rest = beacons[1:]
    shifts = [(0, 0, 0)]
    while next:
        aligned = next.pop()
        tmp = []
        for candidate in rest:
            r = try_align(aligned, candidate)
            if r:
                (updated, shift) = r
                shifts.append(shift)
                next.append(updated)
            else:
                tmp.append(candidate)
        rest = tmp
    return max(sum(abs(a - b) for (a, b) in zip(l, r)) for l, r in itertools.product(shifts, shifts))


data = get_and_write_data(19, 2021)
beacons = parse(data)
print_output(part1(beacons), part2(beacons))
