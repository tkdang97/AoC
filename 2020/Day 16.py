from utils.data import *
import re


def parse(data):
    rules, own, nearby = data.split("\n\n")
    rule_intervals = {}
    for field, low1, high1, low2, high2 in re.findall(r"([\w\s]+):\s(\d+)\-(\d+)\sor\s(\d+)\-(\d+)\n?", rules):
        rule_intervals[field] = [(int(low1), int(high1)), (int(low2), int(high2))]

    return (
        rule_intervals,
        list(map(int, own.splitlines()[1].split(","))),
        [list(map(int, line.split(","))) for line in nearby.splitlines()[1:]],
    )


def part1(rules, nearby):
    valid = set()
    for rule_list in rules.values():
        for low, high in rule_list:
            valid = valid.union(range(low, high + 1))

    res = 0
    for ticket in nearby:
        for val in ticket:
            if val not in valid:
                res += val
    return res


def part2(rules, own, nearby):
    valid = set()
    field_values = {}
    for field, rule_list in rules.items():
        valid_values = set(range(rule_list[0][0], rule_list[0][1] + 1)) | set(
            range(rule_list[1][0], rule_list[1][1] + 1)
        )
        valid |= valid_values
        field_values[field] = valid_values

    invalid = set()
    for i, ticket in enumerate(nearby):
        for val in ticket:
            if val not in valid:
                invalid.add(i)
                break
    valid_tickets = [ticket for i, ticket in enumerate(nearby) if i not in invalid]
    columns = list(zip(*valid_tickets))
    mapping = {}
    while len(mapping) < len(field_values):
        done_fields = set(mapping.values())
        for field, values in field_values.items():
            if field not in done_fields:
                possible = []
                for i, column in enumerate(columns):
                    if i not in mapping and all(val in values for val in column):
                        possible.append(i)
                if len(possible) == 1:
                    mapping[possible[0]] = field

    res = 1
    for pos, field in mapping.items():
        if field.startswith("departure"):
            res *= own[pos]
    return res


test = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""

data = get_and_write_data(16, 2020)
rules, own, nearby = parse(data)
print_output(part1(rules, nearby), part2(rules, own, nearby))
