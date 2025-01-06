from utils.data import *
from sympy.ntheory.modular import crt


def parse(data):
    start, buses = data.splitlines()
    return int(start), buses


def part1(start, buses):
    mods = sorted((int(bus) - start % int(bus), int(bus)) for bus in buses.split(",") if bus != "x")
    mod, id = mods[0]
    return mod * id


def part2(buses):
    buses = [(int(bus), i) for i, bus in enumerate(buses.split(",")) if bus != "x"]
    mods = []
    remainders = []
    for id, offset in buses:
        mods.append(id)
        remainders.append(-offset)
    res = crt(mods, remainders)
    return res[0]


test = """939
7,13,x,x,59,x,31,19
"""

data = get_and_write_data(13, 2020)
start, buses = parse(data)
print_output(part1(start, buses), part2(buses))
