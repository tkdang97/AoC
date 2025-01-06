from utils.data import *


def parse(data):
    return tuple(map(int, data.splitlines()))


def trial(key):
    value = 1
    i = 0
    while value != key:
        value = (value * 7) % 20201227
        i += 1
    return i


def part1(keys):
    card, door = keys
    value = 1
    i = 0
    while value != door:
        value = (value * 7) % 20201227
        i += 1
    subject = card
    value = 1
    for _ in range(i):
        value = (value * subject) % 20201227
    return value


def part2():
    pass


test = """5764801
17807724
"""

data = get_and_write_data(25, 2020)
keys = parse(data)
print_output(part1(keys), part2())
