from utils.data import *
from math import prod
from collections import deque


def parse(data: str) -> str:
    return "".join([f"{int(c, 16):0>4b}" for c in data.strip()])


def decode_literal(packet: str, curr_index: int) -> tuple[int, int]:
    res = 0
    while curr_index < len(packet):
        num = int(packet[curr_index + 1: curr_index + 5], 2)
        res = res << 4 | num
        if packet[curr_index] == "0":
            curr_index += 5
            break
        curr_index += 5
    return res, curr_index


def decode_packet(packet: str, curr_index: int, res: list[list[int, int, int, int]], limit: int) -> int:
    if limit <= curr_index:
        return curr_index
    version = int(packet[curr_index: curr_index + 3], 2)
    type_id = int(packet[curr_index + 3: curr_index + 6], 2)
    curr_index += 6
    if type_id == 4:
        num, curr_index = decode_literal(packet, curr_index)
        res.append([version, type_id, num, 0])
    else:
        res.append([version, type_id, -1, 0])
        res_index = len(res) - 1
        if packet[curr_index] == "0":
            num_bits = int(packet[curr_index + 1: curr_index + 16], 2)
            curr_index += 16
            end = curr_index + num_bits
            num_packets = 0
            while curr_index < end:
                num_packets += 1
                curr_index = decode_packet(packet, curr_index, res, end)
        else:
            num_packets = int(packet[curr_index + 1: curr_index + 12], 2)
            curr_index += 12
            for _ in range(num_packets):
                curr_index = decode_packet(packet, curr_index, res, len(packet))
        res[res_index][3] = num_packets
    return curr_index


def part1(packet: str) -> int:
    res = []
    decode_packet(packet, 0, res, len(packet))
    return sum(r[0] for r in res)


def part2(packet: str) -> int:
    res = []
    decode_packet(packet, 0, res, len(packet))
    ops = {0: sum, 1: prod, 2: min, 3: max,
           5: lambda x: int(x[0] > x[1]), 6: lambda x: int(x[0] < x[1]), 7: lambda x: int(x[0] == x[1])}
    tmp = deque()
    for _, type_id, val, num_packets in reversed(res):
        if type_id == 4:
            tmp.appendleft(val)
        else:
            tmp.appendleft(ops[type_id]([tmp.popleft() for _ in range(num_packets)]))
    return tmp[0]


data = get_and_write_data(16, 2021)
packet = parse(data)
print_output(part1(packet), part2(packet))
