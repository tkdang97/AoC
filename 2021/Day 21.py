from utils.data import *
from functools import cache
from itertools import product
from collections import Counter


def parse(data: str) -> list[int]:
    return [int(line.split(": ")[1]) for line in data.splitlines()]


def part1(pos1: int, pos2: int, score1: int = 0, score2: int = 0, num_rolls: int = 0) -> int:
    if score2 >= 1000:  # only need to check score2 because the other score is not incremented in a recursive call
        return score1 * num_rolls
    new_pos = (pos1 + 3 * num_rolls + 6 - 1) % 10 + 1
    return part1(pos2, new_pos, score2, score1 + new_pos, num_rolls + 3)


def roll_counts(num_throws: int = 3, num_sides: int = 3):
    return Counter(sum(tup) for tup in product(range(1, num_sides + 1), repeat=num_throws))


@cache
def search(pos1: int, pos2: int, score1: int, score2: int) -> tuple[int, int]:
    """
    pos1 and score1 represent the player whose turn it is, so in a recursive call player 1 and player 2
    can just be swapped and there is no need to track the turn player explicitly
    """
    if score2 >= 21:
        return 0, 1
    res = (0, 0)
    global counts
    for steps, count in counts.items():
        new_pos = (pos1 + steps - 1) % 10 + 1
        s1, s2 = search(pos2, new_pos, score2, score1 + new_pos)
        res = (res[0] + count * s2, res[1] + count * s1)
    return res


def part2(pos1: int, pos2: int) -> int:
    scores = search(pos1, pos2, 0, 0)
    return max(scores)


data = get_and_write_data(21, 2021)
positions = parse(data)
counts = roll_counts()
print_output(part1(*positions), part2(*positions))
