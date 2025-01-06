from utils.data import *
from collections import deque


def parse(data):
    return list(map(int, data.splitlines()))


def part1(nums, window=25):
    curr = deque(nums[:window])
    for num in nums[window:]:
        prev_set = set(curr)
        for prev in curr:
            if num - prev in prev_set:
                break
        else:
            return num
        curr.popleft()
        curr.append(num)


def part2(nums):
    target = part1(nums, 25)
    curr = deque()
    curr_sum = 0
    for num in nums:
        if curr_sum == target:
            return min(curr) + max(curr)
        curr.append(num)
        curr_sum += num
        while curr_sum > target:
            curr_sum -= curr.popleft()


test = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""

data = get_and_write_data(9, 2020)
nums = parse(data)
print_output(part1(nums), part2(nums))
