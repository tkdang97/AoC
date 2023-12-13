from utils.data import get_and_write_data


def parse(data):
    res = []
    for line in data.splitlines():
        if line:
            res.append(tuple(line.split()))
    return res


def score(opponent, own):
    shape_score = 1 if own == "X" else 2 if own == "Y" else 3
    if ord(own) == ord(opponent) + (ord('X') - ord('A')):
        return shape_score + 3
    else:
        return shape_score + ((ord(own) - ord(opponent)) % 3 == 0) * 6


def part1(matches):
    return sum(score(*match) for match in matches)


def part2(matches):
    total = 0
    for opponent, own in matches:
        if own == "Y":
            chosen = chr(ord(opponent) + (ord('X') - ord('A')))
        elif own == "X":
            chosen = "X" if opponent == "B" else "Y" if opponent == "C" else "Z"
        else:
            chosen = "X" if opponent == "C" else "Y" if opponent == "A" else "Z"
        total += score(opponent, chosen)
    return total


data = get_and_write_data(2, 2022)
matches = parse(data)
print(f"Part 1: {part1(matches)}")
print(f"Part 2: {part2(matches)}")