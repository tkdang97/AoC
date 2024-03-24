from utils.data import *
import re


def parse(data):
    tunnels = {}  # map from valve to connected valves
    rates = {}  # map from valve to flow rate of valve, only store valves with flow rate over 0
    for valve, rate, neighbours in re.findall(r"Valve (\S+) has flow rate=(\d+); tunnels? leads? to valves? (.+)", data):
        tunnels[valve] = set(neighbours.split(", "))
        if int(rate) > 0:
            rates[valve] = int(rate)

    # set one (different) bit for each valve to store which valves have been visited as a single number
    indices = {valve: 1 << i for i, valve in enumerate(rates)}

    # calculate minimum distances between two valves
    distances = {valve: {neighbour: 1 if neighbour in tunnels[valve] else float("inf") for neighbour in tunnels} for valve in tunnels}
    for valve in distances:
        for i in distances:
            for j in distances:
                distances[i][j] = min(distances[i][j], distances[i][valve] + distances[valve][j])
    return tunnels, rates, indices, distances


def visit(curr_valve, time_left, state, curr_rate, answer):
    global tunnels, rates, indices, distances
    # store maximum possible pressure release values for sets of visited nodes
    answer[state] = max(answer.get(state, 0), curr_rate)
    for valve in rates:
        new_time = time_left - distances[curr_valve][valve] - 1  # -1 because the valve needs to be opened
        if indices[valve] & state or new_time <= 0:
            continue
        visit(valve, new_time, state | indices[valve], curr_rate + new_time * rates[valve], answer)
    return answer


def part1():
    return max(visit("AA", 30, 0, 0, {}).values())


def part2():
    visited = visit("AA", 26, 0, 0, {})
    return max(v1 + v2 for k1, v1 in visited.items() for k2, v2 in visited.items() if not k1 & k2)


data = get_and_write_data(16, 2022)
tunnels, rates, indices, distances = parse(data)
print_output(part1(), part2())
