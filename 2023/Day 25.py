from utils.data import *
from math import prod
import networkx as nx


def parse(data):
    res = nx.Graph()
    for line in data.splitlines():
        left, right = line.split(": ")
        for node in right.split():
            res.add_edge(left, node)
    return res


def part1(graph):
    graph.remove_edges_from(nx.minimum_edge_cut(graph))
    return prod(len(comp) for comp in nx.connected_components(graph))


data = get_and_write_data(25, 2023)
graph = parse(data)
print(part1(graph))
