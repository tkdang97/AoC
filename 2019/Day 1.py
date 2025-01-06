from utils.data import *


def parse(data):
    return list(map(int, data.splitlines()))


def part1(masses):
    return sum(mass // 3 - 2 for mass in masses)


def part2(masses):
    res = 0
    for mass in masses:
        while mass > 0:
            mass = mass // 3 - 2
            if mass > 0:
                res += mass
    return res


test = """14
1969
100756
"""

data = get_and_write_data(1, 2019)
masses = parse(data)
print_output(part1(masses), part2(masses))
