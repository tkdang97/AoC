from utils.data import *


def parse(data):
    return data.splitlines()


def part1(nums):
    cols = zip(*nums)
    gamma = epsilon = ""
    for col in cols:
        gamma += "1" if col.count("1") > col.count("0") else "0"
        epsilon += "0" if col.count("1") > col.count("0") else "1"
    return int(gamma, 2) * int(epsilon, 2)


def part2(nums):
    curr = nums.copy()
    idx = 0
    while len(curr) > 1:
        col = [num[idx] for num in curr]
        keep = "1" if col.count("1") >= col.count("0") else "0"
        curr = list(filter(lambda x: x[idx] == keep, curr))
        idx += 1
    oxy = curr[0]
    curr = nums.copy()
    idx = 0
    while len(curr) > 1:
        col = [num[idx] for num in curr]
        keep = "0" if col.count("0") <= col.count("1") else "1"
        curr = list(filter(lambda x: x[idx] == keep, curr))
        idx += 1
    return int(oxy, 2) * int(curr[0], 2)


data = get_and_write_data(3, 2021)
nums = parse(data)
print_output(part1(nums), part2(nums))