import re


def seed_to_location(input):
    current = list(map(int, input[0].split(":")[1].split()))  # initial seed numbers as integers
    tmp = []
    found = set()
    for line in input[2:]:
        if not line:
            tmp.extend(c for c in current if c not in found)
            current = tmp
            tmp = []
            found = set()
        elif re.match(r"(\w+)-to-(\w+) map:", line):
            continue
        else:
            dest, source, rng = list(map(int, line.split()))
            for cur in current:
                if cur not in found:
                    if source <= cur < source + rng:
                        found.add(cur)
                        tmp.append(dest + (cur - source))
    return current


def find_overlap(start1, size1, start2, size2):
    end1 = start1 + size1
    end2 = start2 + size2

    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)

    if overlap_start < overlap_end:
        overlap_size = overlap_end - overlap_start
        return overlap_start, overlap_size
    else:
        return None


def merge_ranges(ranges):
    sorted_ranges = sorted(ranges)
    res = []
    for start, rng in sorted_ranges:
        if res:
            prev_end = res[-1][0] + res[-1][1]
            if prev_end >= start:
                prev_start, prev_rng = res.pop()
                res.append((prev_start, max(prev_rng, start - prev_start + rng)))
            else:
                res.append((start, rng))
        else:
            res.append((start, rng))
    return res


def fill_ranges(found):
    res = []
    for (start, rng), ranges in found.items():
        if ranges:
            sorted_range = sorted(ranges.keys())
            if sorted_range[0][0] > start:
                res.append((start, sorted_range[0][0] - start))
            res.append(ranges[sorted_range[0]])
            for i in range(1, len(sorted_range)):
                prev_end = sorted_range[i - 1][0] + sorted_range[i - 1][1]
                if sorted_range[i][0] > sorted_range[i - 1][0] + sorted_range[i - 1][1]:  # Non-overlapping ranges
                    res.append((prev_end, sorted_range[i][0] - prev_end))
                res.append(ranges[sorted_range[i]])
            range_end = sorted_range[-1][0] + sorted_range[-1][1]
            if start + rng > range_end:
                res.append((range_end, start + rng - range_end))
        else:
            res.append((start, rng))
    return merge_ranges(res)


def seed_range_to_location(input):
    current = [(int(m[1]), int(m[2])) for m in re.finditer(r"(\d+) (\d+)", input[0].split(":")[1])]
    found = dict()
    for line in input[2:]:
        if not line:
            current = fill_ranges(found)
            found = dict()
        elif re.match(r"(\w+)-to-(\w+) map:", line):
            continue
        else:
            dest, source, rng = list(map(int, line.split()))
            for start, cur_rng in current:
                if (start, cur_rng) not in found:
                    found[(start, cur_rng)] = dict()
                overlap = find_overlap(start, cur_rng, source, rng)
                if overlap:
                    dest_start = dest + overlap[0] - source
                    found[(start, cur_rng)][overlap] = (dest_start, overlap[1])
    return current


with open("inputs/input_5.txt") as f:
    inp = f.read().splitlines()
    locations = seed_to_location(inp)
    range_locations = seed_range_to_location(inp)

print(f"Part 1: {min(locations)}")
print(f"Part 2: {range_locations[0][0]}")
