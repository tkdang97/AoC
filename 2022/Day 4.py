from utils.data import get_and_write_data, print_output
import re


def parse(data):
    res = []
    for line in data.splitlines():
        m = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line)
        if m:
            res.append(((int(m[1]), int(m[2])), (int(m[3]), int(m[4]))))
    return res


def part1(pairs):
    total = 0
    for (s1, e1), (s2, e2) in pairs:
        if (s1 <= s2 and e1 >= e2) or (s2 <= s1 and e2 >= e1):
            total += 1
    return total


def part2(pairs):
    total = 0
    for (s1, e1), (s2, e2) in pairs:
        if e1 >= s2 and e2 >= s1:
            total += 1
    return total


data = get_and_write_data(4, 2022)
pairs = parse(data)
print_output(part1(pairs), part2(pairs))
