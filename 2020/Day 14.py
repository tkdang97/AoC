from utils.data import *
import re
from itertools import product


def parse(data):
    return [line.split(" = ") for line in data.splitlines()]


def part1(instructions):
    mask = ""
    res = {}
    for instruction, value in instructions:
        if instruction == "mask":
            mask = value
        else:
            address = re.search(r"(\d+)", instruction).group(1)
            val = bin(int(value))[2:].zfill(36)
            result_num = []
            for m, v in zip(mask, val):
                if m != "X":
                    result_num.append(m)
                else:
                    result_num.append(v)
            res[address] = int("".join(result_num), 2)
    return sum(res.values())


def part2(instructions):
    mask = ""
    res = {}
    for instruction, value in instructions:
        if instruction == "mask":
            mask = value
        else:
            address = re.search(r"(\d+)", instruction).group(1)
            value = int(value)
            bin_address = bin(int(address))[2:].zfill(36)
            result_address = []
            floating_positions = []
            for i, (m, v) in enumerate(zip(mask, bin_address)):
                if m == "1":
                    result_address.append(m)
                elif m == "0":
                    result_address.append(v)
                else:
                    floating_positions.append(i)
                    result_address.append("")

            for comb in product("01", repeat=len(floating_positions)):
                for pos, val in zip(floating_positions, comb):
                    result_address[pos] = val
                res[int("".join(result_address), 2)] = value
    return sum(res.values())


test = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

data = get_and_write_data(14, 2020)
instructions = parse(data)
print_output(part1(instructions), part2(instructions))
