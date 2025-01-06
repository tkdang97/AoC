from utils.data import *
from collections import deque
from itertools import islice


def parse(data):
    data_deck1, data_deck2 = data.split("\n\n")
    _, *cards1 = data_deck1.splitlines()
    _, *cards2 = data_deck2.splitlines()
    return deque(map(int, cards1)), deque(map(int, cards2))


def part1(deck1, deck2):
    d1, d2 = deck1.copy(), deck2.copy()
    while d1 and d2:
        card1 = d1.popleft()
        card2 = d2.popleft()
        if card1 > card2:
            d1.append(card1)
            d1.append(card2)
        else:
            d2.append(card2)
            d2.append(card1)
    final = d1 if d1 else d2
    return sum(val * (len(final) - i) for i, val in enumerate(final))


def game(deck1, deck2):
    seen = set()
    while deck1 and deck2:
        check = (tuple(deck1), tuple(deck2))
        if check in seen:
            return True
        seen.add(check)
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if len(deck1) >= card1 and len(deck2) >= card2:
            p1_win = game(deque(islice(deck1, 0, card1)), deque(islice(deck2, 0, card2)))
        else:
            p1_win = card1 > card2
        if p1_win:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    return len(deck1) > 0


def part2(deck1, deck2):
    d1, d2 = deck1.copy(), deck2.copy()
    game(d1, d2)
    final = d1 if d1 else d2
    return sum(val * (len(final) - i) for i, val in enumerate(final))


test = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

data = get_and_write_data(22, 2020)
deck1, deck2 = parse(data)
print_output(part1(deck1, deck2), part2(deck1, deck2))
