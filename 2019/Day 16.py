from utils.data import *


def parse(data):
    return list(map(int, data))


def part1():
    pattern = [0, 1, 0, -1]
    curr = nums.copy()
    for _ in range(100):
        out = []
        for i in range(1, len(curr) + 1):
            res = 0
            for j, num in enumerate(curr):
                res += num * pattern[((j + 1) // i) % 4]
            out.append(abs(res) % 10)
        curr = out
    return "".join(map(str, curr))[:8]


def part2():
    offset = sum(10 ** (6 - i) * num for i, num in enumerate(nums[:7]))
    expanded = nums * 10000
    n = len(expanded)
    for _ in range(100):
        partial_sum = sum(expanded[j] for j in range(offset, n))
        for j in range(offset, n):
            t = partial_sum
            partial_sum -= expanded[j]
            expanded[j] = abs(t) % 10
    return "".join(map(str, expanded[offset : offset + 8]))


test = """03036732577212944063491565474664"""

data = get_and_write_data(16, 2019)
nums = parse(data)
print_output(part1(), part2())
