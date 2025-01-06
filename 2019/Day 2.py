from utils.data import *


def parse(data):
    return list(map(int, data.split(",")))


def execute(code, input1, input2):
    code[1] = input1
    code[2] = input2
    curr = 0
    while curr < len(code):
        if code[curr] == 1 and curr < len(code) - 3:
            code[code[curr + 3]] = code[code[curr + 1]] + code[code[curr + 2]]
        elif code[curr] == 2 and curr < len(code) - 3:
            code[code[curr + 3]] = code[code[curr + 1]] * code[code[curr + 2]]
        else:
            break
        curr += 4
    return code[0]


def part1(codes):
    code = codes.copy()
    return execute(code, 12, 2)


def part2(codes):
    for input1 in range(100):
        for input2 in range(100):
            code = codes.copy()
            if execute(code, input1, input2) == 19690720:
                return 100 * input1 + input2
    return None


test = """1,9,10,3,2,3,11,0,99,30,40,50"""

data = get_and_write_data(2, 2019)
codes = parse(data)
print_output(part1(codes), part2(codes))
