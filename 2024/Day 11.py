from utils.data import *
from functools import cache


def parse(data):
    return list(map(int, data.split()))


@cache
def count_stones(num, num_iters):
    if num_iters == 0:
        return 1
    num_str = str(num)
    if num == 0:
        return count_stones(1, num_iters - 1)
    elif len(num_str) & 1 == 1:
        return count_stones(num * 2024, num_iters - 1)
    else:
        return count_stones(int(num_str[: len(num_str) // 2]), num_iters - 1) + count_stones(int(num_str[len(num_str) // 2 :]), num_iters - 1)


def part1(stones):
    return sum(count_stones(stone, 25) for stone in stones)


def part2(stones):
    return sum(count_stones(stone, 75) for stone in stones)


test = """125 17"""

data = get_and_write_data(11, 2024)
stones = parse(data)
print_output(part1(stones), part2(stones))
