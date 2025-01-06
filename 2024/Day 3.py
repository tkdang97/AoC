from utils.data import *
import re


def part1(data):
    instructions = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
    return sum(int(n1) * int(n2) for n1, n2 in instructions)


def part2(data):
    instructions = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", data)
    enabled = True
    res = 0
    for instruction in instructions:
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        elif enabled:
            n1, n2 = re.findall(r"\d+", instruction)
            res += int(n1) * int(n2)
    return res


test = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
test2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

data = get_and_write_data(3, 2024)
print_output(part1(data), part2(data))
