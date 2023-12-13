from utils.data import *
import re
from itertools import zip_longest


class List:
    def __init__(self, outer=None, values=None):
        self.outer = outer  # reference to outer list (parent)
        self.values = [] if values is None else values

    def append(self, value):
        self.values.append(value)

    def __str__(self):
        elements = []
        for val in self.values:
            elements.append(val.__str__())
        return "[" + ",".join(elements) + "]"

    def __lt__(self, other, depth=0, debug=False):
        indent = "\t" * depth
        if debug:
            print(f"{indent}- Compare {self.__str__()} vs {other.__str__()}")
        for val1, val2 in zip_longest(self.values, other.values, fillvalue=None):
            if val1 is None:
                if debug:
                    print(f"{indent}\t- Left side ran out of items, so inputs are in the right order")
                return True
            if val2 is None:
                if debug:
                    print(f"{indent}\t- Right side ran out of items, so inputs are not in the right order")
                return False
            if debug:
                print(f"{indent}\t- Compare {val1.__str__()} vs {val2.__str__()}")
            if isinstance(val1, int) and isinstance(val2, int):
                if val1 < val2:
                    if debug:
                        print(f"{indent}\t\t- Left side is smaller, so inputs are in the right order")
                    return True
                elif val2 < val1:
                    if debug:
                        print(f"{indent}\t\t- Right side is smaller, so inputs are not in the right order")
                    return False
            else:
                if isinstance(val1, int):
                    val1 = List(values=[val1])
                    if debug:
                        print(f"{indent}\t\t- Mixed types; convert left to {val1.__str__()} and retry comparison")
                elif isinstance(val2, int):
                    val2 = List(values=[val2])
                    if debug:
                        print(f"{indent}\t\t- Mixed types; convert right to {val2.__str__()} and retry comparison")
                cmp = val1.__lt__(val2, depth + 2, debug)
                if cmp is None:
                    continue
                else:
                    return cmp
        return None


def parse_line(line: str, li: List):
    curr_digit = []
    for c in line:
        if c.isdigit():
            curr_digit.append(c)
        else:
            if curr_digit:
                li.append(int("".join(curr_digit)))
                curr_digit = []
            if c == "[":  # new list in the list
                tmp = List(li)
                li.append(tmp)
                li = tmp
            elif c == "]":  # inner list finished, return to outer list
                li = li.outer


def parse(data):
    res = []
    for p1, p2 in re.findall(r"\[(.*)\]\n\[(.*)\](?:$|\n)", data):
        list1 = List()
        list2 = List()
        parse_line(p1 + ",", list1)
        parse_line(p2 + ",", list2)
        res.append((list1, list2))
    return res


def part1(pairs, debug=False):
    if debug:
        total = 0
        for i, (p1, p2) in enumerate(pairs, 1):
            print(f"\n== Pair {i} ==")
            if p1.__lt__(p2, debug=True):
                total += i
        return total
    else:
        return sum(i for i, (p1, p2) in enumerate(pairs, 1) if p1 < p2)


def part2(pairs):
    packets = []
    for pair in pairs:
        packets.extend(pair)
    div_packet1 = List(values=[List(values=[2])])
    div_packet2 = List(values=[List(values=[6])])
    packets.extend((div_packet1, div_packet2))
    packets.sort()
    i1 = i2 = 0
    for i, packet in enumerate(packets, 1):
        if packet == div_packet1:
            i1 = i
        elif packet == div_packet2:
            i2 = i
            break
    return i1 * i2


data = get_and_write_data(13, 2022)
pairs = parse(data)
print_output(part1(pairs), part2(pairs))
