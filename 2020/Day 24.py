from utils.data import *
from collections import Counter
import re


DIRS = {"e": (0, 1), "se": (1, 0), "sw": (1, -1), "w": (0, -1), "nw": (-1, 0), "ne": (-1, 1)}


def parse(data):
    return [re.findall(r"e|se|sw|w|nw|ne", line) for line in data.splitlines()]


def part1(tiles):
    black = set()
    for steps in tiles:
        x, y = 0, 0
        for step in steps:
            dx, dy = DIRS[step]
            x += dx
            y += dy
        if (x, y) in black:
            black.remove((x, y))
        else:
            black.add((x, y))
    return len(black)


def simulate_day(black):
    black_adjacent = Counter()
    for x, y in black:
        for dx, dy in DIRS.values():
            black_adjacent[(x + dx, y + dy)] += 1

    new_black = set()
    for coord, count in black_adjacent.items():
        if coord in black:  # check previously black tile
            if count == 1 or count == 2:
                new_black.add(coord)
        else:
            if count == 2:
                new_black.add(coord)
    return new_black


def part2(tiles):
    black = set()
    for steps in tiles:
        x, y = 0, 0
        for step in steps:
            dx, dy = DIRS[step]
            x += dx
            y += dy
        if (x, y) in black:
            black.remove((x, y))
        else:
            black.add((x, y))

    for i in range(100):
        black = simulate_day(black)
        # print(f"Day {i + 1}: {len(black)}")
    return len(black)


test = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""

data = get_and_write_data(24, 2020)
tiles = parse(data)
print_output(part1(tiles), part2(tiles))
