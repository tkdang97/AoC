from utils.data import *


def parse(data):
    res = []
    for line in data.splitlines():
        if line == "noop":
            res.append((1, 0))
        else:
            res.append((2, int(line.split()[-1])))
    return res


def execute(ops):
    res = [1]
    for t, val in ops:
        res.append(res[-1])
        if t == 2:
            res.append(res[-1] + val)
    return res


def part1(registers):
    res = 0
    for i, val in enumerate(registers, 1):
        if i % 40 == 20:
            res += i * val
    return res


def part2(registers):
    res = [["."] * 40 for _ in range(6)]
    for i, val in enumerate(registers):
        row, pos = divmod(i, 40)
        if pos in (val - 1, val, val + 1):
            res[row][pos] = "#"
    for line in res:
        print("".join(line))


data = get_and_write_data(10, 2022)
ops = parse(data)
register_values = execute(ops)
print_output(part1(register_values), part2(register_values))