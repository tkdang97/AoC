from utils.data import *


def parse(data):
    left, right = data.split("-")
    return int(left), int(right)


def part1(left, right):
    count = 0
    for num in range(left, right + 1):
        num_str = str(num)
        if list(num_str) == sorted(num_str) and len(set(num_str)) < len(num_str):
            count += 1
    return count


def part2(left, right):
    count = 0
    for num in range(left, right + 1):
        num_str = str(num)
        if list(num_str) == sorted(num_str) and any(num_str.count(s) == 2 for s in num_str):
            count += 1
    return count


test = """"""

data = get_and_write_data(4, 2019)
bounds = parse(data)
print_output(part1(*bounds), part2(*bounds))
