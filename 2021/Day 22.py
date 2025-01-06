from utils.data import *
from collections import Counter
import re


def parse(data: str) -> list[tuple[int, int, int, int, int, int, int]]:
    return [tuple(map(int, line)) for line in
            re.findall(r"(\d) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)",
                       data.replace("on", "1").replace("off", "0"))]


def check_overlap(min1: int, max1: int, min2: int = -50, max2: int = 50) -> tuple[int, int] | None:
    if max1 >= min2 and max2 >= min1:
        overlap_min = max(min1, min2)
        overlap_max = min(max1, max2)
        return overlap_min - min2, overlap_max + max2 + 1
    else:
        return None


def part1(steps: list[tuple[int, int, int, int, int, int, int]]) -> int:
    res = [[[0] * 101 for _ in range(101)] for _ in range(101)]
    for change, min_x, max_x, min_y, max_y, min_z, max_z in steps:
        x_over = check_overlap(min_x, max_x)
        y_over = check_overlap(min_y, max_y)
        z_over = check_overlap(min_z, max_z)
        if x_over and y_over and z_over:
            for x in range(x_over[0], x_over[1]):
                for y in range(y_over[0], y_over[1]):
                    for z in range(z_over[0], z_over[1]):
                        res[x][y][z] = change
    return sum(sum(sum(sub) for sub in sub1) for sub1 in res)


def part2(steps: list[tuple[int, int, int, int, int, int, int]]) -> int:
    cubes = Counter()
    for change, min_x, max_x, min_y, max_y, min_z, max_z in steps:
        update = Counter()
        sign = 1 if change else -1
        # check for overlaps with existing cubes
        for (min_cx, max_cx, min_cy, max_cy, min_cz, max_cz), csign in cubes.items():
            min_ux = max(min_x, min_cx)
            max_ux = min(max_x, max_cx)
            min_uy = max(min_y, min_cy)
            max_uy = min(max_y, max_cy)
            min_uz = max(min_z, min_cz)
            max_uz = min(max_z, max_cz)
            if min_ux <= max_ux and min_uy <= max_uy and min_uz <= max_uz:
                update[(min_ux, max_ux, min_uy, max_uy, min_uz, max_uz)] -= csign
        if sign == 1:
            update[(min_x, max_x, min_y, max_y, min_z, max_z)] += sign
        cubes.update(update)
        for bounds, val in cubes.copy().items():
            if val == 0:
                del cubes[bounds]

    return sum((max_x - min_x + 1) * (max_y - min_y + 1) * (max_z - min_z + 1) * sign
               for (min_x, max_x, min_y, max_y, min_z, max_z), sign in cubes.items())


data = get_and_write_data(22, 2021)
steps = parse(data)
print_output(part1(steps), part2(steps))
