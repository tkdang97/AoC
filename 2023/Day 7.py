from collections import Counter
from functools import cmp_to_key


def parse(file):
    bids = []
    for line in file:
        hand, bid = line.split()
        bids.append((hand, int(bid)))
    return bids


def hand_value(hand):
    global with_jokers
    counter = Counter(hand)
    if with_jokers and "J" in counter:
        jokers = counter["J"]
        del counter["J"]
        if len(counter) == 0:
            counter["A"] = 5
        else:
            highest, _ = counter.most_common()[0]
            counter[highest] += jokers
    counts = list(counter.values())
    if 5 in counts:
        return 7
    if 4 in counts:
        return 6
    if len(counts) == 2:
        return 5
    if 3 in counts:
        return 4
    if counts.count(2) == 2:
        return 3
    if counts.count(2) == 1:
        return 2
    return 1


def compare(hand_tuple1, hand_tuple2):
    global card_scores

    hand1 = hand_tuple1[0]
    hand2 = hand_tuple2[0]

    hand1_value = hand_value(hand1)
    hand2_value = hand_value(hand2)

    if hand1_value > hand2_value:
        return 1
    elif hand1_value < hand2_value:
        return -1

    for c1, c2 in zip(hand1, hand2):
        if card_scores[c1] < card_scores[c2]:
            return 1
        elif card_scores[c1] > card_scores[c2]:
            return -1
    return 0


def custom_sort(hand_tuples, order):
    global card_scores
    card_scores = {l: i for i, l in enumerate(order)}
    return sorted(hand_tuples, key=cmp_to_key(compare))


def calculate_winnings(hand_tuples, order):
    total = 0
    for rank, (_, bid) in enumerate(custom_sort(hand_tuples, order), 1):
        total += rank * bid
    return total


with open("inputs/input_7.txt") as f:
    hand_tuples = parse(f)

card_scores = {}
with_jokers = False
print(f"Part 1: {calculate_winnings(hand_tuples, 'AKQJT98765432')}")

with_jokers = True
print(f"Part 2: {calculate_winnings(hand_tuples, 'AKQT98765432J')}")
