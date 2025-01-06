from utils.data import *
import re


def parse(data):
    return re.findall(r"(\d+)\-(\d+)\s(\w):\s(\w+)", data)


def part1(rules):
    res = 0
    for minimum, maximum, letter, password in rules:
        cnt = password.count(letter)
        if int(minimum) <= cnt <= int(maximum):
            res += 1
    return res


def part2(rules):
    res = 0
    for pos1, pos2, letter, password in rules:
        p1 = password[int(pos1) - 1] == letter
        p2 = password[int(pos2) - 1] == letter
        if p1 != p2:
            res += 1
    return res


test = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""

data = get_and_write_data(2, 2020)
rules = parse(data)
print_output(part1(rules), part2(rules))
