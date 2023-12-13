from utils.data import *
from collections import defaultdict
import re
import operator
import copy
from math import lcm


def parse(data):
    res = defaultdict(dict)
    curr = -1
    for line in data.splitlines():
        if line:
            m = re.match(r"Monkey (\d+)", line)
            if m:
                curr = int(m[1])
            elif "Starting" in line:
                res[curr]["items"] = list(map(int, line.split(":")[-1].split(",")))
            elif "Operation" in line:
                m = re.search(r"old ([+*]) (\d+|old)", line)
                res[curr]["op"] = (operator.add if m[1] == "+" else operator.mul, None if m[2] == "old" else int(m[2]))
            elif "Test" in line:
                m = re.search(r"divisible by (\d+)", line)
                res[curr]["Test"] = int(m[1])
            else:
                m = re.search(r"throw to monkey (\d+)", line)
                if "true" in line:
                    res[curr][True] = int(m[1])
                else:
                    res[curr][False] = int(m[1])
    return res


def simulate_round(monkeys, manage):
    res = [0] * len(monkeys)
    for monkey in sorted(monkeys.keys()):
        for item in monkeys[monkey]["items"]:
            if monkeys[monkey]["op"][1] is None:
                second_val = item
            else:
                second_val = monkeys[monkey]["op"][1]
            new_val = manage(monkeys[monkey]["op"][0](item, second_val))
            test_res = new_val % monkeys[monkey]["Test"] == 0
            target_monkey = monkeys[monkey][test_res]
            monkeys[target_monkey]["items"].append(new_val)
            res[monkey] += 1
        monkeys[monkey]["items"] = []
    return res


def solve(monkeys, manage, rounds):
    num_ops = [0] * len(monkeys)
    cpy = copy.deepcopy(monkeys)
    for i in range(rounds):
        num_ops = list(map(operator.add, num_ops, simulate_round(cpy, manage)))
    sorted_ops = sorted(num_ops)
    print(num_ops)
    return sorted_ops[-1] * sorted_ops[-2]


def part1(monkeys):
    return solve(monkeys, lambda x: x // 3, 20)


def part2(monkeys):
    least = lcm(*[monkeys[monkey]["Test"] for monkey in monkeys])
    return solve(monkeys, lambda x, val=least: x % least, 10000)


data = get_and_write_data(11, 2022)
monkeys = parse(data)
print_output(part1(monkeys), part2(monkeys))