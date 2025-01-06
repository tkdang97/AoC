from utils.data import *
from collections import Counter


def parse(data):
    return sorted(map(int, data.splitlines()))


def part1(joltages):
    prev = 0
    diffs = Counter()
    for joltage in joltages:
        diffs[joltage - prev] += 1
        prev = joltage
    diffs[3] += 1
    return diffs[1] * diffs[3]


def part2(joltages):
    target = joltages[-1] + 3
    counts = Counter({0: 1})
    for num in joltages + [target]:
        counts[num] = counts[num - 1] + counts[num - 2] + counts[num - 3]
    return counts[target]


test = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""

data = get_and_write_data(10, 2020)
joltages = parse(data)
print_output(part1(joltages), part2(joltages))
