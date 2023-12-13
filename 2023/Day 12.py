from utils.data import *
from functools import cache


def parse(data):
    res = []
    for line in data.splitlines():
        symbols, nums = line.split()
        res.append([symbols, list(map(int, nums.split(",")))])
    return res


@cache
def count_possibilities(line, groups, pos, curr_group_size, finished_hashes):
    if pos == len(line):  # check if all groups of #s are accounted for
        res = 1 if len(groups) == finished_hashes else 0
    elif line[pos] == "#":
        res = count_possibilities(line, groups, pos + 1, curr_group_size + 1, finished_hashes)
    elif line[pos] == "." or finished_hashes == len(groups):
        if finished_hashes < len(groups) and curr_group_size == groups[finished_hashes]:
            res = count_possibilities(line, groups, pos + 1, 0, finished_hashes + 1)
        elif curr_group_size == 0:
            res = count_possibilities(line, groups, pos + 1, 0, finished_hashes)
        else:
            res = 0
    else:
        # count number of possibilities if you replace the ? with a #
        hash_count = count_possibilities(line, groups, pos + 1, curr_group_size + 1, finished_hashes)
        # count number of possibilities if you replace the . with a #,
        # only if a group of #s has just been finished or a . came right before
        dot_count = 0
        if curr_group_size == groups[finished_hashes]:
            dot_count = count_possibilities(line, groups, pos + 1, 0, finished_hashes + 1)
        elif curr_group_size == 0:
            dot_count = count_possibilities(line, groups, pos + 1, 0, finished_hashes)
        res = hash_count + dot_count
    return res


def part1(rows):
    return sum(count_possibilities(line + ".", tuple(groups), 0, 0, 0) for line, groups in rows)


def part2(rows):
    return sum(count_possibilities("?".join([line] * 5) + ".", tuple(groups * 5), 0, 0, 0) for line, groups in rows)


data = get_and_write_data(12, 2023)
rows = parse(data)
print_output(part1(rows), part2(rows))