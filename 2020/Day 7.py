from utils.data import *
from collections import defaultdict


def parse(data):
    outer_bags = defaultdict(list)
    for line in data.splitlines():
        rule = line.split()
        inner = f"{rule[0]} {rule[1]}"
        for i in range(4, len(rule), 4):
            outer = f"{rule[i + 1]} {rule[i + 2]}"
            if rule[i] == "no":
                outer_bags[inner] = []
            else:
                outer_bags[inner].append((outer, int(rule[i])))
    return outer_bags


def part1(bags):
    res = 0
    for inner in bags.values():
        curr = [i[0] for i in inner]
        for bag in curr:
            if bag == "shiny gold":
                res += 1
                break
            curr.extend([i[0] for i in bags[bag]])
    return res


def part2(bags):
    curr = [("shiny gold", 1)]
    for bag, count in curr:
        for inner, inner_count in bags[bag]:
            curr.append((inner, inner_count * count))
    return sum(i[1] for i in curr) - 1


test = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

data = get_and_write_data(7, 2020)
bags = parse(data)
print_output(part1(bags), part2(bags))
