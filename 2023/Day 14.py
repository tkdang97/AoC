from utils.data import *
import copy


def parse(data):
    return list(map(list, data.splitlines()))


def slide(grid):
    for j in range(len(grid[0])):
        free_i = 0
        for i in range(len(grid)):
            if grid[i][j] == "#":
                free_i = i + 1
            elif grid[i][j] == "O":
                grid[i][j] = "."
                grid[free_i][j] = "O"
                free_i += 1


def calculate_weight(grid):
    n = len(grid)
    return sum((n - i) * row.count("O") for i, row in enumerate(grid))


def part1(grid):
    grid_cpy = copy.deepcopy(grid)
    slide(grid_cpy)
    return calculate_weight(grid_cpy)


def rotate_grid(grid):
    return [col[::-1] for col in map(list, zip(*grid))]


def to_str(grid):
    return "".join("".join(row) for row in grid)


def part2(grid):
    grid_cpy = copy.deepcopy(grid)
    seen = {}
    target = 1000000000
    i = 1
    while True:
        for _ in range(4):
            slide(grid_cpy)
            grid_cpy = rotate_grid(grid_cpy)
        s = to_str(grid_cpy)
        if s in seen:
            cycle_length = i - seen[s][0]
            print(f"Cycle detected after {i} iterations with length {cycle_length}")
            for idx, weight in seen.values():
                if idx >= seen[s][0] and idx % cycle_length == target % cycle_length:
                    return weight
        seen[s] = (i, calculate_weight(grid_cpy))
        i += 1


data = get_and_write_data(14, 2023)
grid = parse(data)
print_output(part1(grid), part2(grid))
