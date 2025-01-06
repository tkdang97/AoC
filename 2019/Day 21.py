from utils.data import *
from utils.intcode import run


def parse(data):
    return list(map(int, data.split(",")))


def run_instructions(instructions):
    ins = "\n".join(instructions)
    program = run(codes.copy())
    out = next(program)
    while True:
        try:
            if out == "input":
                for c in ins:
                    out = program.send(ord(c))
                out = program.send(10)
            else:
                if out >= 256:
                    return out
                print(chr(out), end="")
                out = next(program)
        except StopIteration:
            print("Failed")
            break


def part1():
    return run_instructions(["OR C J","AND B J","AND A J","NOT J J","AND D J","WALK"])


def part2():
    return run_instructions(["NOT H J", "OR C J","AND B J","AND A J","NOT J J","AND D J","RUN"])


test = """"""

data = get_and_write_data(21, 2019)
codes = parse(data)
print_output(part1(), part2())
