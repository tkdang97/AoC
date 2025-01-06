from utils.data import *


def parse(data):
    res = []
    for line in data.splitlines():
        split = line.split()
        if split[-1] == "stack":
            res.append((0, 0))
        elif split[-2] == "cut":
            res.append((1, int(split[-1])))
        else:
            res.append((2, int(split[-1])))
    return res


def new_stack(deck, n):
    return deck[::-1]


def cut(deck, n):
    cutoff = n if n >= 0 else len(deck) + n
    return deck[cutoff:] + deck[:cutoff]


def increment(deck, n):
    l = len(deck)
    res = [0] * l
    for i, num in enumerate(deck):
        res[(i * n) % l] = num
    return res


def part1():
    ops = {0: new_stack, 1: cut, 2: increment}
    curr = deck
    for code, num in instructions:
        curr = ops[code](curr, num)
    return curr.index(2019)


def reverse_deal(deck_size, idx, n):
    return deck_size - 1 - idx


def reverse_cut(deck_size, idx, n):
    return (idx + n + deck_size) % deck_size


def reverse_increment(deck_size, idx, n):
    return pow(n, -1, deck_size) * idx % deck_size


def reverse(deck_size, idx):
    ops = {0: reverse_deal, 1: reverse_cut, 2: reverse_increment}
    for code, num in reversed(instructions):
        idx = ops[code](deck_size, idx, num)
    return idx


def part2():
    D = 119315717514047
    N = 101741582076661
    X = 2020
    Y = reverse(D, X)
    Z = reverse(D, Y)
    A = (Y - Z) * pow(X - Y, -1, D) % D
    B = (Y - A * X) % D
    return (pow(A, N, D) * X + (pow(A, N, D) - 1) * pow(A - 1, -1, D) * B) % D


test = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""

data = get_and_write_data(22, 2019)
instructions = parse(data)
deck = list(range(10007))
print_output(part1(), part2())
