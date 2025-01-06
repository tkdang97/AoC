from utils.data import *
from collections import defaultdict, deque


def parse(data):
    return list(map(int, data.splitlines()))


def evolve(num):
    mod = 16777216
    num = ((num * 64) ^ num) % mod
    num = ((num // 32) ^ num) % mod
    num = ((num * 2048) ^ num) % mod
    return num


def part1(nums):
    res = 0
    for num in nums:
        for _ in range(2000):
            num = evolve(num)
        res += num
    return res


def part2(nums):
    total_map = defaultdict(int)
    for num in nums:
        prev_digit = num % 10
        diffs = deque()
        seen = set()
        for _ in range(2000):
            num = evolve(num)
            digit = num % 10
            diffs.append(digit - prev_digit)
            if len(diffs) > 4:
                diffs.popleft()
            if len(diffs) == 4:
                sequence = tuple(diffs)
                if sequence not in seen:
                    seen.add(sequence)
                    total_map[sequence] += digit
            prev_digit = digit
    return max(total_map.values())


test = """1
2
3
2024
"""

data = get_and_write_data(22, 2024)
nums = parse(data)
print_output(part1(nums), part2(nums))
