from utils.data import *


def parse(data):
    return [int(num) for num in data.splitlines()]


def mix(numbers, num_shuffles=1, multiplier=1):
    original = [(i, num * multiplier) for i, num in enumerate(numbers)]
    res = original.copy()
    n = len(numbers)
    for _ in range(num_shuffles):
        for tup in original:
            idx = res.index(tup)
            new_idx = (idx + tup[1]) % (n - 1)
            if new_idx == 0 and 0 < idx:
                new_idx = n - 1
            elif new_idx == n - 1 and new_idx > idx:
                new_idx = 0
            if idx != new_idx:
                removed = res.pop(idx)
                res.insert(new_idx, removed)
    return [val[1] for val in res]


def part1(numbers):
    mixed = mix(numbers)
    zero_idx = mixed.index(0)
    return sum(mixed[(zero_idx + num) % len(mixed)] for num in (1000, 2000, 3000))


def part2(numbers):
    mixed = mix(numbers, num_shuffles=10, multiplier=811589153)
    zero_idx = mixed.index(0)
    return sum(mixed[(zero_idx + num) % len(mixed)] for num in (1000, 2000, 3000))


data = get_and_write_data(20, 2022)
nums = parse(data)
test = [1, 2, -3, 3, -2, 0, 4]
print_output(part1(nums), part2(nums))
