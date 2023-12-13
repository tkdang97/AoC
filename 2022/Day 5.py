from utils.data import get_and_write_data, print_output
import copy
import re


def parse(data):
    res = []
    steps = []
    crates, procedures = data.split("\n\n")
    for line in crates.splitlines():
        for i, crate in enumerate(re.findall(r"\[(\w)\]|\s{4}", line)):
            if len(res) <= i:
                res.append([])
            if crate:
                res[i].append(crate)

    for line in procedures.splitlines():
        m = re.match(r"move (\d+) from (\d+) to (\d+)", line)
        if m:
            steps.append((int(m[1]), int(m[2]) - 1, int(m[3]) - 1))
    return [stack[::-1] for stack in res], steps


def solve(crates, procedures, part1=True):
    tmp = copy.deepcopy(crates)
    for num, src, dest in procedures:
        tmp[dest].extend(tmp[src][-num:][::-1] if part1 else tmp[src][-num:])
        tmp[src] = tmp[src][:-num]
    return "".join(stack[-1] for stack in tmp)


data = get_and_write_data(5, 2022)
crates, procedures = parse(data)
print_output(solve(crates, procedures), solve(crates, procedures, False))
