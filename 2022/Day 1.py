from utils.data import get_and_write_data


def parse(data):
    res = [sum(map(int, inventory.split())) for inventory in data.split("\n\n")]
    return res


def part1(inventories):
    return max(inventories)


def part2(inventories):
    return sum(sorted(inventories)[-3:])


data = get_and_write_data(1, 2022)
inventories = parse(data)
print(f"Part 1: {part1(inventories)}")
print(f"Part 2: {part2(inventories)}")
