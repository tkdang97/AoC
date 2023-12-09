from collections import defaultdict
from math import prod
from re import finditer


def parse(text, parts):
    symbols = {(r, c) for r in range(len(text))
               for c in range(len(text[0].strip()))
               if text[r][c] not in '01234566789.'}

    for r, row in enumerate(text):
        for m in finditer(r'\d+', row):
            next_set = {(r+s, c+d) for s in (-1, 0, 1)
                        for d in (-1, 0, 1)
                        for c in range(m.start(), m.end())}
            for c in next_set & symbols:
                parts[c].append(int(m[0]))


with open("inputs/input_3.txt") as f:
    parts = defaultdict(list)
    txt = f.readlines()
    parse(txt, parts)

print(f"Part 1: {sum(sum(p) for p in parts.values())}")
print(f"Part 2: {sum(prod(p) for (r, c), p in parts.items() if len(p) == 2 and txt[r][c] == '*')}")
