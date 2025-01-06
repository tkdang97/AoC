from utils.data import *
from math import log10
import re


def parse(data):
    equations = []
    for line in data.splitlines():
        result, rest = line.split(":")
        equations.append((int(result), list(map(int, re.findall("\d+", rest)))))
    return equations


def check_equation(result, nums, part2=False):
    if len(nums) == 0:
        return False
    if len(nums) == 1:
        return result == nums[0]
    # intermediate = {nums[0]}
    # for num in nums[1:]:
    #     next_nums = set()
    #     for prev in intermediate:
    #         next_nums.add(prev + num)
    #         next_nums.add(prev * num)
    #         if part2:
    #             next_nums.add(int(f"{prev}{num}"))
    #     intermediate = next_nums
    # return result in intermediate
    last = nums[-1]
    possible = False
    if result % last == 0:
        possible |= check_equation(result // last, nums[:-1], part2)
        
    if part2:
        # For concatenation, check if the last digits of result equal the last number
        pow_10 = 10 ** (int(log10(last)) + 1)
        if (result - last) % pow_10 == 0:
            possible |= check_equation(result // pow_10, nums[:-1], part2)
    
    possible |= check_equation(result - last, nums[:-1], part2)
    return possible
    


def part1(equations):
    res = 0
    for result, nums in equations:
        if check_equation(result, nums):
            res += result
    return res


def part2(equations):
    res = 0
    for result, nums in equations:
        if check_equation(result, nums, True):
            res += result
    return res


test = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

data = get_and_write_data(7, 2024)
equations = parse(data)
print_output(part1(equations), part2(equations))
