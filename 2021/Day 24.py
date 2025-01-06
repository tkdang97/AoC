from utils.data import *


VARS = {"w": 0, "x": 1, "y": 2, "z": 3}


def parse(data):
    return [line.split() for line in data.splitlines()]


def solve(inp, instructions):
    stack = []
    for i in range(14):
        div, chk, add = map(int, [instructions[i * 18 + x][-1] for x in [4, 5, 15]])
        if div == 1:
            stack.append((i, add))
        elif div == 26:
            j, add = stack.pop()
            inp[i] = inp[j] + add + chk
            if inp[i] > 9:
                inp[j] -= inp[i] - 9
                inp[i] = 9
            if inp[i] < 1:
                inp[j] += 1 - inp[i]
                inp[i] = 1

    return "".join(map(str, inp))


def part1(instructions):
    return solve([9] * 14, instructions)


def part2(instructions):
    return solve([1] * 14, instructions)


test = """"""
data = get_and_write_data(24, 2021)
instructions = parse(data)
print_output(part1(instructions), part2(instructions))
