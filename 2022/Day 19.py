import re
from utils.data import *


def parse(data):
    return [list(map(int, re.findall(r"\d+", line))) for line in data.splitlines()]


# from https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tls7a/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
def search(start, minutes, blueprints, quality=True):
    res = start
    max_geodes = [(t - 1) * t // 2 for t in range(minutes + 1)]
    for bp_id, a, b, c, d, e, f in blueprints:
        m = 0
        max_ore, max_clay, max_obsidian = max(a, b, c, e), d, f

        def dfs(t, g,  # t:time remaining, g:goal robot type
                i, j, k, l,  # i:ore, j:clay, k:obsidian, l:geode robots
                w, x, y, z):  # w:ore, x:clay, y:obsidian, z:geode available
            nonlocal m
            if (g == 0 and i >= max_ore or
                    g == 1 and j >= max_clay or
                    g == 2 and (k >= max_obsidian or j == 0) or
                    g == 3 and k == 0 or
                    z + l * t + max_geodes[t] <= m):
                return
            while t:
                if g == 0 and w >= a:
                    for g in range(4):
                        dfs(t - 1, g, i + 1, j, k, l, w - a + i, x + j, y + k, z + l)
                    return
                elif g == 1 and w >= b:
                    for g in range(4):
                        dfs(t - 1, g, i, j + 1, k, l, w - b + i, x + j, y + k, z + l)
                    return
                elif g == 2 and w >= c and x >= d:
                    for g in range(4):
                        dfs(t - 1, g, i, j, k + 1, l, w - c + i, x - d + j, y + k, z + l)
                    return
                elif g == 3 and w >= e and y >= f:
                    for g in range(4):
                        dfs(t - 1, g, i, j, k, l + 1, w - e + i, x + j, y - f + k, z + l)
                    return
                t, w, x, y, z = t - 1, w + i, x + j, y + k, z + l
            m = max(m, z)

        for g in range(4):
            dfs(minutes, g, 1, 0, 0, 0, 0, 0, 0, 0)
        if quality:
            res += m * bp_id
        else:
            res *= m
    return res


def part1(blueprints):
    return search(0, 24, blueprints, True)


def part2(blueprints):
    return search(1, 32, blueprints[:3], False)


data = get_and_write_data(19, 2022)
blueprints = parse(data)
print_output(part1(blueprints), part2(blueprints))
