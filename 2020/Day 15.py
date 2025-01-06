from utils.data import *


def parse(data):
    return list(map(int, data.split(",")))


def solve(nums, turns):
    last = nums[-1]
    seen = {num: i for i, num in enumerate(nums)}
    for i in range(len(nums) - 1, turns - 1):
        seen[last], last = i, i - seen[last] if last in seen else 0
    return last


def part1(nums):
    return solve(nums, 2020)


def part2(nums):
    return solve(nums, 30000000)


test = """0,3,6"""

data = get_and_write_data(15, 2020)
nums = parse(data)
print_output(part1(nums), part2(nums))
