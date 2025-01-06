from utils.data import *


def parse(data):
    return list(map(int, data.splitlines()))


def part1(expenses):
    number_set = set(expenses)
    res = 0
    for num in expenses:
        if 2020 - num in number_set:
            res = num * (2020 - num)
            break
    return res


def part2(expenses):
    number_set = set(expenses)
    for i, num in enumerate(expenses):
        for num2 in expenses[i + 1 :]:
            if (2020 - num - num2) in number_set:
                return num * num2 * (2020 - num - num2)
    return 0


test = """1721
979
366
299
675
1456
"""

data = get_and_write_data(1, 2020)
expenses = parse(data)
print_output(part1(expenses), part2(expenses))
