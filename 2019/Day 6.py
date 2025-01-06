from utils.data import *
from collections import defaultdict
from functools import cache


def parse(data):
    orbits = defaultdict(list)
    for line in data.splitlines():
        center, planet = line.split(")")
        orbits[center].append(planet)
    return orbits


@cache
def count_orbits(planet):
    if planet not in orbits:
        return 0, 0
    direct = len(orbits[planet])
    indirect = 0
    for orbiting in orbits[planet]:
        next_direct, next_indirect = count_orbits(orbiting)
        direct += next_direct
        indirect += next_indirect + next_direct
    return direct, indirect


def part1():
    return sum(count_orbits("COM"))


def part2():
    orbiting = {}
    for center, planets in orbits.items():
        for planet in planets:
            orbiting[planet] = center
    curr = [orbiting["YOU"]]
    target = orbiting["SAN"]
    seen = {"YOU"}
    steps = 0
    while curr:
        nxt = []
        for planet in curr:
            if planet == target:
                return steps
            seen.add(planet)
            if planet in orbiting and orbiting[planet] not in seen:
                nxt.append(orbiting[planet])
            for orbiting_planet in orbits[planet]:
                if orbiting_planet not in seen:
                    nxt.append(orbiting_planet)
        curr = nxt
        steps += 1
    return steps


test = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""

data = get_and_write_data(6, 2019)
orbits = parse(data)
print_output(part1(), part2())
