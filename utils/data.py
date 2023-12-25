from aocd import get_data
from functools import wraps
import time
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


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} took {total_time:.4f} seconds')
        return result
    return timeit_wrapper
