from utils.data import *
from collections import defaultdict


digits = {0: set("abcefg"), 1: set("cf"), 2: set("acdeg"), 3: set("acdfg"), 4: set("bcdf"),
          5: set("abdfg"), 6: set("abdefg"), 7: set("acf"), 8: set("abcdefg"), 9: set("abcdfg")}
rev_digits = {tuple(sorted(v)): k for k, v in digits.items()}


def parse(data):
    inputs = []
    outputs = []
    for line in data.splitlines():
        inp, out = line.split(" | ")
        inputs.append(inp.strip().split(" "))
        outputs.append(out.strip().split(" "))
    return inputs, outputs


def part1(outputs):
    return sum(sum(len(digit) in (2, 3, 4, 7) for digit in line) for line in outputs)


def decode(input, output):
    mapping = {}
    length_groups = defaultdict(list)
    for inp in input:
        length_groups[len(inp)].append(set(inp))
    # 7 is only digit with 3 segments, 1 is only digit with 2, the only differing segment between the two is a
    a = (length_groups[3][0] - length_groups[2][0]).pop()
    mapping[a] = "a"
    # the common segments between digits with 5 segments are a, d, g while 4 only has d out of these
    common_five = set.intersection(*length_groups[5])
    d = (common_five & length_groups[4][0]).pop()
    mapping[d] = "d"
    # since a and d are now known, g can be extracted from the 5 segement digits
    g = (common_five - {a, d}).pop()
    mapping[g] = "g"
    # common segements between digits with 6 segments are a, b, f, g and since a and g are known, f and b can be figured out by comparing with digit 1
    common_six = set.intersection(*length_groups[6])
    f = ((common_six - {a, g}) & length_groups[2][0]).pop()
    mapping[f] = "f"
    b = (common_six - {a, f, g}).pop()
    mapping[b] = "b"
    # since f is now known, c can be found by looking at digit 1
    c = (length_groups[2][0] - {f}).pop()
    mapping[c] = "c"
    # now only e is remaining
    e = (length_groups[7][0] - {a, b, c, d, f, g}).pop()
    mapping[e] = "e"

    res = 0
    for out in output:
        res = res * 10 + rev_digits[tuple(sorted(mapping[c] for c in out))]
    return res


def part2(inputs, outputs):
    return sum(decode(*data) for data in zip(inputs, outputs))


data = get_and_write_data(8, 2021)
inputs, outputs = parse(data)
print_output(part1(outputs), part2(inputs, outputs))
