import re
from utils.data import *
from operator import lt, gt


def parse(data):
    workflows, parts = data.split("\n\n")
    parts = [{var: int(val) for var, val in re.findall(r"(\w+)=(\d+)", line)} for line in parts.splitlines()]
    workflows = {wf.split("{")[0]: wf.split("{")[1][:-1] for wf in workflows.splitlines()}
    return workflows, parts


def eval_workflow(workflows, wf_name, part):
    for rule in workflows[wf_name].split(","):
        if rule == "R":
            return False
        if rule == "A":
            return True
        if ":" not in rule:
            return eval_workflow(workflows, rule, part)
        condition, res = rule.split(":")
        if "<" in condition:
            var, value = condition.split("<")
            value = int(value)
            comp = lt
        else:
            var, value = condition.split(">")
            value = int(value)
            comp = gt
        if comp(part[var], value):
            if res == "R":
                return False
            if res == "A":
                return True
            return eval_workflow(workflows, res, part)


def part1(workflows, parts):
    return sum(sum(part.values()) for part in parts if eval_workflow(workflows, "in", part))


def check_workflow(wf_name):
    global workflows
    return check_cases(workflows[wf_name].split(","))


def check_case(var, is_gt, value, ranges):
    pos = "xmas".index(var)
    res = []
    for rng in ranges:
        rng = list(rng)
        low, high = rng[pos]
        if is_gt:
            low = max(low, value + 1)
        else:
            high = min(high, value - 1)
        if low <= high:
            rng[pos] = (low, high)
            res.append(tuple(rng))
    return res


def check_cases(rules):
    rule = rules[0]
    # check cases without comparisons, if rejected, then there is nothing to check for the case
    # if accepted then start with the base ranges of 1 to 4000
    if rule == "R":
        return []

    # if accepted then start with the base ranges of 1 to 4000
    if rule == "A":
        return [[(1, 4000), (1, 4000), (1, 4000), (1, 4000)]]

    # if it is another workflow then recurse into that workflow
    if ":" not in rule:
        return check_workflow(rule)

    # otherwise recursively narrow the ranges for the two different options, one where the current condition
    # is true and another where it is false and return all the range combinations
    condition = rule.split(":")[0]
    is_gt = ">" in condition
    var = condition[0]
    value = int(condition[2:])
    inverted = value + 1 if is_gt else value - 1  # +1/-1 to convert from <= and >= to < and >
    condition_true = check_case(var, is_gt, value, check_cases([rule.split(":")[1]]))
    condition_false = check_case(var, not is_gt, inverted, check_cases(rules[1:]))
    return condition_true + condition_false


def part2():
    res = 0
    for rng in check_workflow("in"):
        val = 1
        for low, high in rng:
            val *= high - low + 1
        res += val
    return res


data = get_and_write_data(19, 2023)
workflows, parts = parse(data)
print_output(part1(workflows, parts), part2())
