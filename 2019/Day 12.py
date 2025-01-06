from utils.data import *
import re
from itertools import count
from math import lcm


def parse(data):
    positions = list(tuple(map(int, tup)) for tup in re.findall(r"(\-?\d+),\sy=(\-?\d+),\sz=(\-?\d+)", data))
    return positions


def time_step(info):
    res = []
    for i, ((x1, y1, z1), (xv1, yv1, zv1)) in enumerate(info):
        dxv = dyv = dzv = 0
        for j, ((x2, y2, z2), _) in enumerate(info):
            if i != j:
                dirx = 0 if x1 == x2 else 1 if x2 > x1 else -1
                diry = 0 if y1 == y2 else 1 if y2 > y1 else -1
                dirz = 0 if z1 == z2 else 1 if z2 > z1 else -1
                dxv, dyv, dzv = dxv + dirx, dyv + diry, dzv + dirz
        new_xv, new_yv, new_zv = xv1 + dxv, yv1 + dyv, zv1 + dzv
        res.append(((x1 + new_xv, y1 + new_yv, z1 + new_zv), (new_xv, new_yv, new_zv)))
    return res


def part1():
    info = [(coords, (0, 0, 0)) for coords in positions]
    for _ in range(100):
        info = time_step(info)
    return sum(sum(map(abs, coords)) * sum(map(abs, velocities)) for coords, velocities in info)


def part2():
    info = [(coords, (0, 0, 0)) for coords in positions]
    initial_x, initial_y, initial_z = zip(*positions)
    x_cycle = y_cycle = z_cycle = None
    for i in count(start=1):
        info = time_step(info)
        xs, ys, zs = zip(*[c[0] for c in info])
        xvs, yvs, zvs = zip(*[c[1] for c in info])
        if not x_cycle and xs == initial_x and all(v == 0 for v in xvs):
            x_cycle = i
            print(x_cycle)
        if not y_cycle and ys == initial_y and all(v == 0 for v in yvs):
            y_cycle = i
            print(y_cycle)
        if not z_cycle and zs == initial_z and all(v == 0 for v in zvs):
            z_cycle = i
            print(z_cycle)
        if x_cycle and y_cycle and z_cycle:
            break
    return lcm(x_cycle, y_cycle, z_cycle)


test = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""

data = get_and_write_data(12, 2019)
positions = parse(data)
print_output(part1(), part2())
