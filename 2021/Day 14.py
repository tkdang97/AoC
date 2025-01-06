from utils.data import *
from collections import Counter
import re


def parse(data):
    template = re.match(r"(\w+)", data).group(1)
    rules = {l: r for l, r in re.findall(r"(\w+) -> (\w+)", data)}
    return template, rules


def step(pairs, chars, rules):
    for pair, count in pairs.copy().items():
        if pair in rules:
            a, b = pair[0], pair[1]
            insert = rules[pair]
            pairs[pair] -= count
            pairs[a + insert] += count
            pairs[insert + b] += count
            chars[insert] += count


def solve(template, rules, steps):
    pairs = Counter(template[i - 1] + template[i] for i in range(1, len(template)))
    chars = Counter(template)
    for i in range(steps):
        step(pairs, chars, rules)
    return max(chars.values()) - min(chars.values())


def part1(template, rules):
    return solve(template, rules, 10)


def part2(template, rules):
    return solve(template, rules, 40)


data = get_and_write_data(14, 2021)
parsed = parse(data)
print_output(part1(*parsed), part2(*parsed))
