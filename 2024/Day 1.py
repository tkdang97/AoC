from utils.data import *
from collections import Counter
import re


def parse(data):
    nums = [[], []]
    for line in data.splitlines():
        num1, num2 = re.match(r"(\d+)\s*(\d+)", line).groups()
        nums[0].append(int(num1))
        nums[1].append(int(num2))
    return nums


def part1(nums):
    dist = 0
    for num1, num2 in zip(sorted(nums[0]), sorted(nums[1])):
        dist += abs(num1 - num2)
    return dist


def part2(nums):
    counts_right = Counter(nums[1])
    similarity = 0
    for num in nums[0]:
        similarity += num * counts_right[num]
    return similarity


test = """3   4
4   3
2   5
1   3
3   9
3   3"""

data = get_and_write_data(1, 2024)
nums = parse(data)
print_output(part1(nums), part2(nums))
