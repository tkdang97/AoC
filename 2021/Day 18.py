from __future__ import annotations
from utils.data import *
from math import floor, ceil
from functools import reduce
from itertools import permutations
from copy import deepcopy


class SnailfishNumber:
    def __init__(self, s: str = "", start: int = 0, depth: int = 0):
        self.parent = None
        self.depth = depth
        if s:
            if s[start + 1].isdigit():
                self.left = int(s[start + 1])
                if s[start + 3].isdigit():
                    self.right = int(s[start + 3])
                    self.end = start + 4
                else:
                    self.right = SnailfishNumber(s, start + 3, self.depth + 1)
                    self.right.parent = self
                    self.end = self.right.end + 1
            else:
                self.left = SnailfishNumber(s, start + 1, self.depth + 1)
                self.left.parent = self
                if s[self.left.end + 2].isdigit():
                    self.right = int(s[self.left.end + 2])
                    self.end = self.left.end + 3
                else:
                    self.right = SnailfishNumber(s, self.left.end + 2, self.depth + 1)
                    self.right.parent = self
                    self.end = self.right.end + 1

    def __add__(self, other: SnailfishNumber) -> SnailfishNumber:
        s = SnailfishNumber()
        s.left, s.left.parent = deepcopy(self), s
        s.right, s.right.parent = deepcopy(other), s
        s.update_depth()
        updated = True
        while updated:
            if s.explode():
                continue
            if s.split():
                continue
            updated = False
        return s

    def __str__(self) -> str:
        left = self.left if isinstance(self.left, int) else self.left.__str__()
        right = self.right if isinstance(self.right, int) else self.right.__str__()
        return f"[{left},{right}]"

    def update_depth(self) -> None:
        """Updates the depth of all pairs after adding two pairs together"""
        for child in (self.left, self.right):
            if isinstance(child, SnailfishNumber):
                child.depth += 1
                child.update_depth()

    def add_to_left(self) -> None:
        """Adds the left number of a pair to the closest number to the left of the pair"""
        prev = self
        while prev.parent and prev.parent.left == prev:
            prev = prev.parent
        prev = prev.parent
        if prev:
            if isinstance(prev.left, int):
                prev.left += self.left
            else:
                prev = prev.left
                while isinstance(prev.right, SnailfishNumber):
                    prev = prev.right
                prev.right += self.left

    def add_to_right(self) -> None:
        """Adds the right number of a pair to the closest number to the right of the pair"""
        prev = self
        while prev.parent and prev.parent.right == prev:
            prev = prev.parent
        prev = prev.parent
        if prev:
            if isinstance(prev.right, int):
                prev.right += self.right
            else:
                prev = prev.right
                while isinstance(prev.left, SnailfishNumber):
                    prev = prev.left
                prev.left += self.right

    def explode(self) -> bool:
        """Checks if any pair has to be exploded and if yes executes the explosion"""
        if self.depth >= 4 and isinstance(self.left, int) and isinstance(self.right, int):
            self.add_to_left()
            self.add_to_right()
            if self.parent.left == self:
                self.parent.left = 0
            else:
                self.parent.right = 0
            return True
        for child in (self.left, self.right):
            if isinstance(child, SnailfishNumber) and child.explode():
                return True
        return False

    def split(self) -> bool:
        """Checks if any pair has to be split and if yes executes the split"""
        if isinstance(self.left, int) and self.left >= 10:
            left = floor(self.left / 2)
            right = ceil(self.left / 2)
            self.left = SnailfishNumber(depth=self.depth + 1)
            self.left.left = left
            self.left.right = right
            self.left.parent = self
            return True
        elif isinstance(self.left, SnailfishNumber) and self.left.split():
            return True
        elif isinstance(self.right, int) and self.right >= 10:
            left = floor(self.right / 2)
            right = ceil(self.right / 2)
            self.right = SnailfishNumber(depth=self.depth + 1)
            self.right.left = left
            self.right.right = right
            self.right.parent = self
            return True
        elif isinstance(self.right, SnailfishNumber) and self.right.split():
            return True
        return False

    def magnitude(self) -> int:
        left = 3 * (self.left if isinstance(self.left, int) else self.left.magnitude())
        right = 2 * (self.right if isinstance(self.right, int) else self.right.magnitude())
        return left + right


def parse(data: str) -> list[SnailfishNumber]:
    return [SnailfishNumber(line) for line in data.splitlines()]


def part1(numbers: list[SnailfishNumber]) -> int:
    res = reduce(SnailfishNumber.__add__, numbers)
    return res.magnitude()


def part2(numbers: list[SnailfishNumber]) -> int:
    return max((a + b).magnitude() for a, b in permutations(numbers, 2))


data = get_and_write_data(18, 2021)
numbers = parse(data)
print_output(part1(numbers), part2(numbers))
