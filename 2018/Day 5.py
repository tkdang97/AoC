from utils.data import *
from string import ascii_lowercase


def parse():
    return data


def react(polymer):
    stack = []
    for unit in polymer:
        if stack and (
            (unit.islower() and stack[-1] == unit.upper()) or (unit.isupper() and stack[-1] == unit.lower())
        ):
            stack.pop()
        else:
            stack.append(unit)
    return len(stack)    


def part1():
    return react(polymer)


def part2():
    return min(react(filter(lambda x: x.lower() != c, polymer)) for c in ascii_lowercase)    


test = """dabAcCaCBAcCcaDA"""

data = get_and_write_data(5, 2018)
polymer = parse()
print_output(part1(), part2())
