from utils.data import get_and_write_data, print_output
from collections import deque


def solve(text, length):
    curr = deque(text[:length])
    for i in range(length, len(text)):
        if len(set(curr)) == length:
            return i
        curr.popleft()
        curr.append(text[i])
    return len(text)


data = get_and_write_data(6, 2022).strip()
print_output(solve(data, 4), solve(data, 14))
