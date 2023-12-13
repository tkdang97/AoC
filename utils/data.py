from aocd import get_data
import os
import os.path as path


def get_and_write_data(day, year):
    data = get_data(day=day, year=year)
    target_dir = path.join(path.abspath(path.join(path.dirname(path.abspath(__file__)), os.pardir)), str(year), "inputs")
    if not path.exists(target_dir):
        os.makedirs(target_dir)
    with open(f"{target_dir}/input_{day}.txt", "w") as f:
        f.write(data)
    return data


def print_output(part1, part2):
    print(f"Part 1: {part1}\nPart 2: {part2}")