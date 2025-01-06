from utils.data import *
import re
from collections import Counter
from functools import cache
from math import ceil


def parse(data):
    needed = {}
    for line in data.splitlines():
        items = re.findall(r"(\d+)\s(\w+)", line)
        produced_qty, produced_item = items[-1]
        needed[produced_item] = (int(produced_qty), [(int(q), i) for q, i in items[:-1]])
    return needed


def get_ores(output, qty, materials):
    if output == "ORE":
        return qty
    produced_qty, requirements = needed[output]
    num_crafts = ceil((qty - materials[output]) / produced_qty)
    needed_ores = 0
    for q, inp in requirements:
        ores = get_ores(inp, q * num_crafts, materials)
        materials[inp] -= q * num_crafts
        needed_ores += ores
    materials[output] += produced_qty * num_crafts
    return needed_ores


def part1():
    return get_ores("FUEL", 1, Counter())


def part2():
    target = available = 10**12
    one_fuel = get_ores("FUEL", 1, Counter())
    total = 0
    curr = available // one_fuel
    while available > one_fuel:
        total += curr
        materials = Counter()
        available -= get_ores("FUEL", curr, materials)
        available += sum(get_ores(k, v, Counter()) for k, v in materials.items() if v > 0 and k != "FUEL")
        curr = available // one_fuel
    if get_ores("FUEL", total, Counter()) > target:
        low = target // one_fuel
        high = total
        while low < high:
            mid = ceil((low + high) / 2)
            if get_ores("FUEL", mid, Counter()) > target:
                high = mid - 1
            else:
                low = mid
        return low # if get_ores("FUEL", low, Counter()) <= target else low - 1
    return total


test = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""

data = get_and_write_data(14, 2019)
needed = parse(data)
print_output(part1(), part2())
