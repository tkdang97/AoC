from utils.data import *
from itertools import permutations, count
from utils.intcode import run


def parse(data):
    return list(map(int, data.split(",")))


def part1():
    max_signal = 0
    for perm in permutations(range(5), 5):
        curr_input = 0
        programs = (run(codes.copy()), run(codes.copy()), run(codes.copy()), run(codes.copy()), run(codes.copy()))
        for phase, prog in zip(perm, programs):
            next(prog)
            prog.send(phase)
            curr_input = prog.send(curr_input)
        max_signal = max(max_signal, curr_input)
    return max_signal


def part2():
    max_signal = 0
    for perm in permutations(range(5, 10), 5):
        programs = (run(codes.copy()), run(codes.copy()), run(codes.copy()), run(codes.copy()), run(codes.copy()))
        for phase, prog in zip(perm, programs):
            next(prog)
            prog.send(phase)

        loop_output = 0
        curr = 0
        for i in count():
            done = False
            for prog in programs:
                try:
                    if i != 0:
                        next(prog)
                    curr = prog.send(curr)
                    if prog == programs[-1]:
                        loop_output = curr
                except StopIteration:
                    done = True
                    break
            if done:
                break

        max_signal = max(max_signal, loop_output)
    return max_signal


test = """3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"""

data = get_and_write_data(7, 2019)
codes = parse(data)
print_output(part1(), part2())
