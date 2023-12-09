from collections import deque


def parse(file):
    res = []
    for line in file:
        if line:
            res.append(list(map(int, line.split())))
    return res


def extrapolate(history):
    ends = 0
    starts = 0
    for sequence in history:
        tmp = deque([deque(sequence)])
        while tmp and any(x != 0 for x in tmp[-1]):
            tmp.append(deque([tmp[-1][i] - tmp[-1][i - 1] for i in range(1, len(tmp[-1]))]))
        tmp[-1].append(0)
        for i in range(len(tmp) - 2, -1, -1):
            tmp[i].append(tmp[i][-1] + tmp[i + 1][-1])
            tmp[i].appendleft(tmp[i][0] - tmp[i + 1][0])
        ends += tmp[0][-1]
        starts += tmp[0][0]
    return ends, starts


with open("inputs/input_9.txt") as f:
    history = parse(f)
    part1, part2 = extrapolate(history)

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
