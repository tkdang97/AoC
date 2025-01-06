from utils.data import *
from statistics import median


left = ["(", "[", "{", "<"]
right = [")", "]", "}", ">"]
bracket_match = {right[i]: left[i] for i in range(4)}


def parse(data):
    return data.splitlines()


def part1(chunks):
    values = {")": 3, "]": 57, "}": 1197, ">": 25137}
    score = 0
    for line in chunks:
        seq = []
        for bracket in line:
            if bracket in left:
                seq.append(bracket)
            else:
                prev = seq.pop()
                if bracket_match[bracket] != prev:
                    score += values[bracket]
                    break
    return score


def part2(chunks):
    rev_brackets = {v: k for k, v in bracket_match.items()}
    scores = []
    for line in chunks:
        seq = []
        corrupted = False
        for bracket in line:
            if bracket in left:
                seq.append(bracket)
            else:
                prev = seq.pop()
                if bracket_match[bracket] != prev:
                    corrupted = True
                    break
        if not corrupted and seq:
            score = 0
            for bracket in reversed(seq):
                score = score * 5 + right.index(rev_brackets[bracket]) + 1
            scores.append(score)
    return int(median(scores))


data = get_and_write_data(10, 2021)
chunks = parse(data)
print_output(part1(chunks), part2(chunks))
