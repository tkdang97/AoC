from collections import defaultdict
from re import findall, match


def parse_line(line):
    res = defaultdict(int)
    game_id = int(match(r"Game (\d+)", line)[1])
    for num, color in findall(r"(\d+) (\w+)", line):
        res[color] = max(res[color], int(num))
    return game_id, res


def is_possible(line):
    game_id, res = parse_line(line)
    if res["red"] <= 12 and res["green"] <= 13 and res["blue"] <= 14:
        return game_id
    return 0


def minimum_set(line):
    game_id, res = parse_line(line)
    return res["red"] * res["green"] * res["blue"]


total = 0
set_sum = 0
with open("inputs/input_2.txt", "r") as f:
    for line in f:
        total += is_possible(line)
        set_sum += minimum_set(line)
print(f"Part 1: {total}")
print(f"Part 2: {set_sum} ")
