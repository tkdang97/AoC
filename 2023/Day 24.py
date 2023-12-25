from utils.data import *
from itertools import combinations
from operator import add
from sympy import Symbol, symbols, solve
import re


def parse(data):
    points = []
    for line in data.splitlines():
        nums = list(map(int, re.findall(r"-?\d+", line)))
        points.append((tuple(nums[:3]), tuple(nums[3:])))
    return points


# Given the two pairs of hailstones and velocities, calculate their slopes and intercepts (linear function y = mx + b)
# and set the functions equal to solve for x and calculate y based on this
def intersection(p1, d1, p2, d2):
    m1 = d1[1] / d1[0]
    b1 = p1[1] - m1 * p1[0]
    m2 = d2[1] / d2[0]
    b2 = p2[1] - m2 * p2[0]
    if m1 == m2:
        return None, None
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return x, y


@timeit
def part1(points, low, high):
    res = 0
    for p1, p2 in combinations(points, 2):
        a, da = p1
        b, db = p2

        # Checking for the intersection between the two linear functions of the hailstones
        x, y = intersection(a, da, b, db)

        if x is None:
            continue

        # Check whether the intersection point lies in the future by checking whether the intersection point
        # lies in the direction of the movement/velocity relative to the starting position for both hailstones
        dx = x - a[0]
        dy = y - a[1]
        if (dx > 0) != (da[0] > 0) or (dy > 0) != (da[1] > 0):
            continue

        dx = x - b[0]
        dy = y - b[1]
        if (dx > 0) != (db[0] > 0) or (dy > 0) != (db[1] > 0):
            continue

        # Checking whether the intersection is in the target area
        if low <= x <= high and low <= y <= high:
            res += 1

    return res


@timeit
def part2(points):
    x, y, z, dx, dy, dz = symbols("x y z dx dy dz")  # 6 Symbols/variables for the stone (starting position and velocity)

    equations = []
    syms = []

    # Checking any three points/hailstones is enough because for every hailstone there will be one additional variable,
    # which is the time when it collides with the stone, here represented by the symbol t_{index}
    # Since you get three equations for each hailstone, using three hailstones then means you have
    # 9 equations for 9 variables to solve for
    for i, point in enumerate(points[:3]):
        (x1, y1, z1), (dx1, dy1, dz1) = point
        t = Symbol(f"t_{i}")

        eqx = x + dx * t - x1 - dx1 * t
        eqy = y + dy * t - y1 - dy1 * t
        eqz = z + dz * t - z1 - dz1 * t

        equations.extend((eqx, eqy, eqz))
        syms.append(t)

    result = solve(equations, *([x, y, z, dx, dy, dz] + syms))
    return sum(result[0][:3])


test = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


data = get_and_write_data(24, 2023)
points = parse(data)
print_output(part1(points, 200000000000000, 400000000000000), part2(points))
