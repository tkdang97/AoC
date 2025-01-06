from utils.data import *
from utils.intcode import run
from itertools import combinations
from collections import deque


def parse(data):
    return list(map(int, data.split(",")))


def part1():
    program = run(codes.copy())
    out = ""
    commands = deque(["west", "take mug", "north", "take easter egg", "south", "east", "south", "east", "north", "take candy cane", 
                "south", "west", "north", "east", "take coin", "north", "north", "take hypercube", "south", "east", "take manifold",
                "west", "south", "south", "east", "take pointer", "west", "west", "take astrolabe", "north", "east", "north"])
    items = ["mug", "easter egg", "candy cane", "coin", "hypercube", "manifold", "pointer", "astrolabe"]
    for n in range(1, len(items)):
        for combination in combinations(items, n):
            for item in items:
                commands.append(f"drop {item}")
            for item in combination:
                commands.append(f"take {item}")
            commands.append("east")
    c = next(program)
    while True:
        try:
            if c == "input":
                print(out)
                out = ""
                inp = commands.popleft()
                for char in inp:
                    c = program.send(ord(char))
                    assert c == "input"
                c = program.send(10)
            else:
                out += chr(c)
                c = next(program)
        except StopIteration:
            print(out)
            break


def part2():
    pass


data = get_and_write_data(25, 2019)
codes = parse(data)
print_output(part1(), part2())
