from utils.data import *
import re


def parse(data):
    res = re.findall(r"([a-zA-Z]+) (\d+)", data)
    return res


def part1(instructions):
    x = y = 0
    for ins, steps in instructions:
        match ins:
            case "forward":
                x += int(steps)
            case "down":
                y += int(steps)
            case "up":
                y -= int(steps)
            case _:
                raise ValueError("Invalid instruction")
    return x * y


def part2(instructions):
    x = y = aim = 0
    for ins, steps in instructions:
        match ins:
            case "forward":
                x += int(steps)
                y += (aim * int(steps))
            case "down":
                aim += int(steps)
            case "up":
                aim -= int(steps)
            case _:
                raise ValueError("Invalid instruction")
    return x * y


data = get_and_write_data(2, 2021)
instructions = parse(data)
print_output(part1(instructions), part2(instructions))
