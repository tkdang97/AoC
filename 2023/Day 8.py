from math import lcm
import re


def parse(text):
    graph = dict()
    path = text[0].strip()
    for line in text[2:]:
        m = re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)
        if m:
            graph[m[1]] = {"L": m[2], "R": m[3]}

    return path, graph


def calculate_steps(path, graph, curr, target):
    steps = 0
    found = False
    while not found:
        for step in path:
            steps += 1
            curr = graph[curr][step]
            if target(curr):
                found = True
                break
    return steps


def part2(path, graph):
    starts = [node for node in graph if node[-1] == "A"]
    num_steps = [calculate_steps(path, graph, node, lambda x: x[-1] == "Z") for node in starts]
    return lcm(*num_steps)


with open("inputs/input_8.txt") as f:
    path, graph = parse(f.readlines())

print(f"Part 1: {calculate_steps(path, graph, 'AAA', lambda x: x == 'ZZZ')}")
print(f"Part 2: {part2(path, graph)}")
