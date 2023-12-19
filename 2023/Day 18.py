from utils.data import *
from itertools import pairwise


# shoelace formula; taking 1/2 of the sum of determinants of consecutive point pairs
def shoelace(points):
    area = 0
    for (x1, y1), (x2, y2) in pairwise(points):
        area += x1 * y2 - x2 * y1
    return area // 2


def parse(data, part1=True):
    global directions
    points = [(0, 0)]
    loc = (0, 0)
    num_pts = 0
    dir_list = list(directions.values())
    for line in data.splitlines():
        if line:
            direction, steps, color = line.split()
            if part1:
                move_dir = directions[direction]
                steps = int(steps)
            else:
                move_dir = dir_list[int(color[-2])]
                steps = int(color[2: 7], 16)
            num_pts += steps
            loc = (loc[0] + steps * move_dir[0], loc[1] + steps * move_dir[1])
            points.append(loc)
    return points, num_pts


def solve(points, num_pts):
    area = shoelace(points)
    b = num_pts

    # Pick's theorem: Area = Interior points (I) + boundary points (b) / 2 - 1
    # --> I = Area - b / 2 + 1, since we also need to count the perimeter, additional +b needed so -b/2 turns to b/2
    return area + b // 2 + 1


directions = {"R": (1, 0), "D": (0, 1), "L": (-1, 0), "U": (0, -1)}
data = get_and_write_data(18, 2023)
print_output(solve(*parse(data)), solve(*parse(data, False)))
