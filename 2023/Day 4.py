from collections import defaultdict


def overlaps(line):
    tickets = line.split(":")[1].split("|")
    winning = set(tickets[0].split())
    nums = set(tickets[1].split())
    return len(winning & nums)


def copies(overlaps, card_num, counter):
    if card_num not in counter:
        counter[card_num] = 1

    for n in range(1, overlaps + 1):
        counter[card_num + n] += counter[card_num]


with open("inputs/input_4.txt") as f:
    total = 0
    counter = defaultdict(lambda: 1)
    for i, line in enumerate(f, 1):
        num_overlaps = overlaps(line)
        total += int(2 ** (num_overlaps - 1))
        copies(num_overlaps, i, counter)

print(f"Part 1: {total}")
print(f"Part 2: {sum(counter.values())}")