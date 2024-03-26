from utils.data import *


values = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def parse(data):
    return data.splitlines()


def convert_from_snafu(s):
    res = 0
    for i, symbol in enumerate(s):
        res += values[symbol] * (5 ** (len(s) - 1 - i))
    return res


def convert_to_snafu(num):
    if num:
        div, rem = divmod(num + 2, 5)
        return convert_to_snafu(div) + "=-012"[rem]
    return ""


def part1(nums):
    total = sum(convert_from_snafu(num) for num in nums)
    return convert_to_snafu(total)


data = get_and_write_data(25, 2022)
nums = parse(data)
print_output(part1(nums))
