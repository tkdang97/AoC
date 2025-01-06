from utils.data import *
from collections import defaultdict
from functools import cache


def parse(data):
    edges = defaultdict(set)
    for line in data.splitlines():
        n1, n2 = line.split("-")
        edges[n1].add(n2)
        edges[n2].add(n1)
    return edges


def part1(edges):
    res = set()
    for node1 in edges:
        for node2 in edges[node1]:
            for node3 in edges[node2]:
                if node1 in edges[node3] and any(node[0] == "t" for node in (node1, node2, node3)):
                    res.add(tuple(sorted((node1, node2, node3))))
    return len(res)


def part2(edges):
    @cache
    def build_set(curr):
        max_set = curr
        check = set(curr)
        for node in curr:
            for node2 in edges[node]:
                if node2 not in check and check.issubset(edges[node2]):
                    new_set = build_set(tuple(sorted(curr + (node2,))))
                    if len(new_set) > len(max_set):
                        max_set = new_set
        return max_set

    res = ()
    for node in edges:
        largest = build_set((node,))
        if len(largest) > len(res):
            res = largest
    return ",".join(sorted(res))


test = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

data = get_and_write_data(23, 2024)
edges = parse(data)
print_output(part1(edges), part2(edges))
