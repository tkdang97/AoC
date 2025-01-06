from utils.data import *
from functools import cache


def parse(data):
    patterns, designs = data.split("\n\n")
    return patterns.split(", "), designs.splitlines()


def part1(patterns, designs):
    def is_possible(design):
        if design == "":
            return True
        possible = False
        for pattern in patterns:
            if design.startswith(pattern):
                possible = possible or is_possible(design[len(pattern):])
        return possible

    res = 0
    for design in designs:
        if is_possible(design):
            res += 1
    return res


def part2(patterns, designs):
    @cache
    def count_ways(design):
        if design == "":
            return 1
        total = 0
        for pattern in patterns:
            if design.startswith(pattern):
                total += count_ways(design[len(pattern):])
        return total

    return sum(count_ways(design) for design in designs)


test = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

data = get_and_write_data(19, 2024)
patterns, designs = parse(data)
print_output(part1(patterns, designs), part2(patterns, designs))
