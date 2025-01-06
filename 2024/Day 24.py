from utils.data import *
from collections import defaultdict
import operator


def parse(data):
    start, rules = data.split("\n\n")
    initial = {}
    for line in start.splitlines():
        wire, val = line.split(": ")
        initial[wire] = int(val)

    gates = {}
    op_map = {"AND": operator.__and__, "OR": operator.__or__, "XOR": operator.__xor__}
    for line in rules.splitlines():
        w1, op, w2, _, out = line.split(" ")
        gates[out] = (w1, op_map[op], w2)
    return initial, gates


def wire_value(wire, values, gates):
    if wire in values:
        return values[wire]

    w1, op, w2 = gates[wire]
    values[wire] = op(wire_value(w1, values, gates), wire_value(w2, values, gates))
    return values[wire]


def part1(initial, gates):
    values = initial.copy()
    for out in gates:
        wire_value(out, values, gates)
    res = 0
    for i, key in enumerate(sorted(k for k in values if k[0] == "z")):
        res |= values[key] << i
    return res


def part2(initial, gates):
    for test_bit in range(46):
        test_values = {}
        i = 1 << test_bit
        out_should = i + i
        for x in range(46):
            test_values["x" + str(x).zfill(2)] = (i >> x) & 1
            test_values["y" + str(x).zfill(2)] = (i >> x) & 1
        for z in range(46):
            if wire_value("z" + str(z).zfill(2), test_values, gates) != (out_should >> z) & 1:
                print("mismatch at bit", z)
                break


test = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""

data = get_and_write_data(24, 2024)
initial, gates = parse(data)
print_output(part1(initial, gates), part2(initial, gates))
