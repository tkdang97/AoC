from utils.data import *
from functools import reduce


def parse(data):
    return data.split(",")


def hash(sequence):
    return reduce(lambda i, c: (i + ord(c)) * 17 % 256, sequence, 0)


def part1(sequences):
    return sum(hash(s) for s in sequences)


def calculate_power(boxes):
    total = 0
    for i, box in enumerate(boxes, 1):
        for j, power in enumerate(box.values(), 1):
            total += i * j * power
    return total


def part2(sequences):
    boxes = [dict() for _ in range(256)]

    for step in sequences:
        match step.strip('-').split('='):
            case [label, strength]:
                boxes[hash(label)][label] = int(strength)
            case [label]:
                boxes[hash(label)].pop(label, 0)
    return calculate_power(boxes)


data = get_and_write_data(15, 2023)
sequences = parse(data)
print_output(part1(sequences), part2(sequences))
