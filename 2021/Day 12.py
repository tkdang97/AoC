from utils.data import *
from collections import defaultdict
import re


def parse(data):
    graph = defaultdict(list)
    for a, b in re.findall(r"(\w+)-(\w+)", data):
        graph[a].append(b)
        graph[b].append(a)
    return graph


def dfs(node, graph, visited, twice):
    if node == "end":
        return 1
    total = 0
    for neigh in graph[node]:
        if neigh not in visited:
            total += dfs(neigh, graph, visited | {neigh} if neigh.islower() else visited, twice)
        elif not twice and neigh != "start":
            total += dfs(neigh, graph, visited, True)
    return total


def part1(graph):
    return dfs("start", graph, {"start"}, True)


def part2(graph):
    return dfs("start", graph, {"start"}, False)


data = get_and_write_data(12, 2021)
graph = parse(data)
print_output(part1(graph), part2(graph))