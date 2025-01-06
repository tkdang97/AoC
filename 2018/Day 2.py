from utils.data import *
from collections import Counter


def parse():
    return data.splitlines()


def part1():
    twos = threes = 0
    for box in boxes:
        counts = Counter(box)
        if 2 in counts.values():
            twos += 1
        if 3 in counts.values():
            threes += 1
    return twos * threes


def part2():
    for box in boxes:
        for box2 in boxes:
            if box != box2:
                diffs = sum(c1 != c2 for c1, c2 in zip(box, box2))
                if diffs == 1:
                    print(box, box2)
                    return "".join(box[i] for i in range(len(box)) if box[i] == box2[i])


test = """"""

data = get_and_write_data(2, 2018)
boxes = parse()
print_output(part1(), part2())
