from utils.data import *
from utils.intcode import run
from collections import defaultdict, deque


def parse(data):
    return list(map(int, data.split(",")))


def part1():
    computers = []
    packets = []
    states = []
    for i in range(50):
        program = run(codes.copy())
        assert next(program) == "input"
        states.append(program.send(i))
        computers.append(program)
        packets.append(deque())

    while True:
        for i, comp in enumerate(computers):
            state = states[i]
            if state == "input":
                if packets[i]:
                    x, y = packets[i].popleft()
                    state = comp.send(x)
                    assert state == "input", "Not in input state after sending x"
                    state = comp.send(y)
                    states[i] = state
                else:
                    states[i] = comp.send(-1)
            else:
                address = state
                x = next(comp)
                y = next(comp)
                if address == 255:
                    return y
                states[i] = next(comp)
                packets[address].append((x, y))


def part2():
    computers = []
    packets = []
    states = []
    nat = None
    prev_nat_y = None
    for i in range(50):
        program = run(codes.copy())
        assert next(program) == "input"
        states.append(program.send(i))
        computers.append(program)
        packets.append(deque())

    while True:
        if nat is not None and all(len(q) == 0 for q in packets) and all(state == "input" for state in states):
            if prev_nat_y and nat[1] == prev_nat_y:
                return nat[1]
            prev_nat_y = nat[1]
            states[0] = computers[0].send(nat[0])
            states[0] = computers[0].send(nat[1])
            nat = None
        for i, comp in enumerate(computers):
            state = states[i]
            if state == "input":
                if packets[i]:
                    x, y = packets[i].popleft()
                    state = comp.send(x)
                    assert state == "input", "Not in input state after sending x"
                    state = comp.send(y)
                    states[i] = state
                else:
                    states[i] = comp.send(-1)
            else:
                address = state
                x = next(comp)
                y = next(comp)
                states[i] = next(comp)

                if address == 255:
                    nat = (x, y)
                else:
                    packets[address].append((x, y))


data = get_and_write_data(23, 2019)
codes = parse(data)
print_output(part1(), part2())
