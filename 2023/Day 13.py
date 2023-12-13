from utils.data import *


def parse(data):
    patterns = []
    curr = []
    for line in data.splitlines() + [""]:
        if line:
            curr.append(line)
        else:
            patterns.append(curr)
            curr = []
    return patterns


def transpose(pattern):
    return list(zip(*pattern))


def pattern_score(pattern, num_differences):
    for i in range(1, len(pattern)):
        num_rows = min(i, len(pattern) - i)
        differences = 0
        for j in range(i - num_rows, i):
            opposite = i + (i - j) - 1
            differences += sum(1 for k in range(len(pattern[j])) if pattern[j][k] != pattern[opposite][k])
        if differences == num_differences:
            return i
    return None


def solve(patterns, num_differences):
    total = 0
    for i, pattern in enumerate(patterns):
        row_score = pattern_score(pattern, num_differences)
        if row_score:
            total += row_score * 100
        else:
            total += pattern_score(transpose(pattern), num_differences)
    return total


def part1(patterns):
    return solve(patterns, 0)


def part2(patterns):
    return solve(patterns, 1)


data = get_and_write_data(13, 2023)
patterns = parse(data)
print_output(part1(patterns), part2(patterns))