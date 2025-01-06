from utils.data import *
from collections import defaultdict, deque


def parse(data):
    disk = []
    pos = {}
    free = {}
    curr_pos = 0
    for i, num in enumerate(data.strip(" \n")):
        length = int(num)
        to_append = i // 2 if i & 1 == 0 else -1
        disk.extend([to_append] * length)
        if to_append == -1:
            free[curr_pos] = length
        else:
            pos[to_append] = (curr_pos, length)
        curr_pos += length
    return disk, pos, free


def part1(disk):
    cpy = disk.copy()
    n = len(cpy)
    first_free = next(i for i, num in enumerate(cpy) if num == -1)
    last = n - 1
    for i in range(n - 1, -1, -1):
        if cpy[i] != -1:
            last = i
            break
    while last > first_free:
        cpy[first_free], cpy[last] = cpy[last], -1
        while first_free < n and cpy[first_free] != -1:
            first_free += 1
        while last > first_free and cpy[last] == -1:
            last -= 1
    result = 0
    for i, num in enumerate(cpy):
        if num == -1:
            break
        result += i * num
    return result


def part2(disk, pos, free):
    cpy = pos.copy()
    for id in sorted(pos.keys(), reverse=True):
        curr_pos, length = pos[id]
        for candidate_pos in sorted(free.keys()):
            if candidate_pos >= curr_pos:
                break
            free_length = free[candidate_pos]
            if free_length >= length:
                cpy[id] = (candidate_pos, length)
                del free[candidate_pos]
                if length < free_length:
                    free[candidate_pos + length] = free_length - length
                break
    rep = [-1] * len(disk)
    for id, (curr_pos, length) in cpy.items():
        for i in range(curr_pos, curr_pos + length, 1):
            rep[i] = id
    result = 0
    for i, num in enumerate(rep):
        if num != -1:
            result += i * num
    return result


test = """2333133121414131402"""

data = get_and_write_data(9, 2024)
disk, pos, free = parse(data)
print_output(part1(disk), part2(disk, pos, free))
