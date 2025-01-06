from utils.data import *


def parse(data):
    return data.splitlines()


def decode(line):
    lower = 0
    upper = 127
    for c in line[:7]:
        mid = (lower + upper) // 2
        if c == "F":
            upper = mid
        else:
            lower = mid + 1

    left = 0
    right = 7
    for c in line[7:]:
        mid = (left + right) // 2
        if c == "L":
            right = mid
        else:
            left = mid + 1

    return lower * 8 + left


def part1(passes):
    return max(decode(line) for line in passes)


def part2(passes):
    ids = {decode(line) for line in passes}
    for id in range(min(ids) + 1, max(ids)):
        if id not in ids:
            return id
    return 0


test = """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
"""

data = get_and_write_data(5, 2020)
passes = parse(data)
print_output(part1(passes), part2(passes))
