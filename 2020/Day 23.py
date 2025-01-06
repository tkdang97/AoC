from utils.data import *


class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class LinkedList:
    def __init__(self, values):
        self.lookup = {}
        self.min = float("inf")
        self.max = 0
        prev = None
        for val in values:
            node = Node(val)
            if prev:
                prev.next = node
            self.lookup[val] = node
            self.min = min(self.min, val)
            self.max = max(self.max, val)
            prev = node
        self.lookup[values[-1]].next = self.lookup[values[0]]


def parse(data):
    return list(map(int, data))


def move(numbers, curr):
    removed = [numbers.lookup[curr].next, numbers.lookup[curr].next.next, numbers.lookup[curr].next.next.next]
    removed_vals = {r.value for r in removed}
    dest = curr - 1
    while dest == 0 or dest in removed_vals:
        dest -= 1
        if dest < numbers.min:
            dest = numbers.max
    numbers.lookup[curr].next = removed[-1].next
    nxt = numbers.lookup[dest].next
    numbers.lookup[dest].next = removed[0]
    removed[-1].next = nxt
    return numbers.lookup[curr].next.value


def part1(numbers):
    nums = LinkedList(numbers)
    curr = numbers[0]
    for _ in range(100):
        curr = move(nums, curr)
    node = nums.lookup[1].next
    res = []
    while node.value != 1:
        res.append(node.value)
        node = node.next
    return "".join(map(str, res))


def part2(numbers):
    nums = LinkedList(numbers + list(range(max(numbers) + 1, 1000001)))
    curr = numbers[0]
    for _ in range(10000000):
        curr = move(nums, curr)
    return nums.lookup[1].next.value * nums.lookup[1].next.next.value


test = """389125467"""

data = get_and_write_data(23, 2020)
numbers = parse(data)
print_output(part1(numbers), part2(numbers))
