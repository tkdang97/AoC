from utils.data import *
from collections import defaultdict, Counter
import re


def parse():
    events = []
    for year, month, day, hour, minute, event in re.findall(
        r"\[(\d{4})\-(\d{2})\-(\d{2})\s(\d{2}):(\d{2})\]\s(.*)\n", data
    ):
        events.append((tuple(map(int, (year, month, day, hour, minute))), event))
    return events


def part1():
    asleep = defaultdict(lambda: Counter())
    sleep_minutes = Counter()
    curr = None
    fell_asleep = None
    for (_, _, _, _, minute), event in sorted(events):
        if "begins" in event:
            curr = int(event.split()[1][1:])
        elif "wakes" in event:
            for m in range(fell_asleep, minute):
                asleep[curr][m] += 1
                sleep_minutes[curr] += 1
        else:
            fell_asleep = minute
    guard = sleep_minutes.most_common(1)[0][0]
    return sorted(asleep[guard], key=lambda x: -asleep[guard][x])[0] * guard, asleep


def part2():
    max_minutes = 0
    guard = None
    target_minute = None
    for id in asleep:
        for minute, count in asleep[id].items():
            if count > max_minutes:
                max_minutes = count
                target_minute = minute
                guard = id
    return guard * target_minute


test = """"""

data = get_and_write_data(4, 2018)
events = parse()
p1, asleep = part1()
print_output(p1, part2())
