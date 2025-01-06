from utils.data import *


def parse(data):
    return list(map(int, data.split(",")))


def run(code, inp):
    outputs = []
    i = 0
    while i < len(code):
        opcode = code[i] % 100
        modes = str(code[i] // 100).zfill(2)[::-1]
        try:
            op1 = code[code[i + 1]] if modes[0] == "0" else code[i + 1]
        except IndexError:
            break
        if opcode in (1, 2, 5, 6, 7, 8):
            op2 = code[code[i + 2]] if modes[1] == "0" else code[i + 2]
        else:
            op2 = 0
        match opcode:
            case 1:
                code[code[i + 3]] = op1 + op2
                i += 4
            case 2:
                code[code[i + 3]] = op1 * op2
                i += 4
            case 3:
                code[code[i + 1]] = inp
                i += 2
            case 4:
                outputs.append(op1)
                i += 2
            case 5:
                if op1 != 0:
                    i = op2
                else:
                    i += 3
            case 6:
                if op1 == 0:
                    i = op2
                else:
                    i += 3
            case 7:
                num = 1 if op1 < op2 else 0
                code[code[i + 3]] = num
                i += 4
            case 8:
                num = 1 if op1 == op2 else 0
                code[code[i + 3]] = num
                i += 4
            case 99:
                break
    return outputs[-1]


def part1(codes):
    return run(codes.copy(), 1)


def part2(codes):
    return run(codes.copy(), 5)


test = """"""

data = get_and_write_data(5, 2019)
codes = parse(data)
print_output(part1(codes), part2(codes))
