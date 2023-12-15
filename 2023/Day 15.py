from utils.data import *


def parse(data):
    return data.split(",")


def hash(sequence):
    res = 0
    for c in sequence:
        res = ((res + ord(c)) * 17) % 256
    return res


def part1(sequences):
    return sum(hash(s) for s in sequences)


def calculate_power(boxes):
    total = 0
    for i, box in enumerate(boxes, 1):
        for j, (_, power) in enumerate(box, 1):
            total += i * j * power
    return total


def part2(sequences):
    boxes = [[] for _ in range(256)]
    pos = {}
    for seq in sequences:
        if "=" in seq:
            label, strength = seq.split("=")
            if label in pos:
                box, idx = pos[label]
                boxes[box][idx][1] = int(strength)
            else:
                box = hash(label)
                pos[label] = (box, len(boxes[box]))
                boxes[box].append([label, int(strength)])
        else:
            label = seq[:-1]
            if label in pos:
                box, idx = pos[label]
                del boxes[box][idx]
                del pos[label]
                for i, (lab, _) in enumerate(boxes[box]):
                    pos[lab] = (box, i)
    return calculate_power(boxes)


data = get_and_write_data(15, 2023)
sequences = parse(data)
print_output(part1(sequences), part2(sequences))
