from utils.data import get_and_write_data
from itertools import islice


def parse(data):
    res = []
    for line in data.splitlines():
        if line:
            res.append(line)
    return res


def calculate_priority(item):
    return ord(item) - ord('a') + 1 + 58 * item.isupper()


def part1(rucksacks):
    total = 0
    for rucksack in rucksacks:
        h1, h2 = rucksack[:len(rucksack) // 2], rucksack[len(rucksack) // 2:]
        item = set(h1).intersection(h2).pop()
        total += calculate_priority(item)
    return total


def batched(iterable, n):
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


def part2(rucksacks):
    total = 0
    for batch in batched(rucksacks, 3):
        item = set.intersection(*map(set, batch))
        print(item)
        total += calculate_priority(item.pop())
    return total


data = get_and_write_data(3, 2022)
rucksacks = parse(data)
print(f"Part 1: {part1(rucksacks)}")
print(f"Part 2: {part2(rucksacks)}")
