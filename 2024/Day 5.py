from utils.data import *
import functools


def parse(data):
    rules, updates = data.split("\n\n")
    rules = [tuple(map(int, rule.split("|"))) for rule in rules.splitlines()]
    updates = [list(map(int, update.split(","))) for update in updates.splitlines()]

    return rules, updates


def sort_update(rules, update):
    def compare(a, b):
        return -1 if (a, b) in rules else 1 if (b, a) in rules else 0
    return sorted(update, key=functools.cmp_to_key(compare))


def part1(rules, updates):
    total = 0
    for update in updates:
        sorted_update = sort_update(rules, update)
        if sorted_update == update:
            total += update[len(update) // 2]
    return total


def part2(rules, updates):
    total = 0
    for update in updates:
        sorted_update = sort_update(rules, update)
        if sorted_update != update:
            total += sorted_update[len(sorted_update) // 2]
    return total


test = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

data = get_and_write_data(5, 2024)
rules, updates = parse(data)
print_output(part1(rules, updates), part2(rules, updates))
