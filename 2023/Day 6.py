def parse(inp):
    times = inp[0].split(":")[1].split()
    dist = inp[1].split(":")[1].split()
    return times, dist


def calc_distance(total_time, pressed_time):
    return (total_time - pressed_time) * pressed_time


def margin(times, dist):
    res = 1
    for time, dst in zip(list(map(int, times)), list(map(int, dist))):
        possibilities = 0
        for i in range(1, time):
            if calc_distance(time, i) > dst:
                possibilities += 1
        res *= possibilities
    return res


def binary_search(time, left, right, target_dist, is_increasing):
    while right - left > 1:
        mid = (left + right) // 2
        potential_dist = calc_distance(time, mid)
        if (is_increasing and potential_dist > target_dist) or (not is_increasing and potential_dist <= target_dist):
            right = mid
        else:
            left = mid + 1
    return left


def single_race(times, dist):
    time = int("".join(times))
    dst = int("". join(dist))
    l, r = 1, time - 1
    while l <= r:  # Find peak of the distances, i.e. the time where the maximum distance can be reached
        mid = (l + r) // 2
        if (mid == 0 or calc_distance(time, mid - 1) <= calc_distance(time, mid)) and \
                (mid == time - 1 or calc_distance(time, mid + 1) <= calc_distance(time, mid)):
            l = mid
            break
        if mid > 0 and calc_distance(time, mid - 1) > calc_distance(time, mid):
            r = mid - 1
        else:
            l = mid + 1
    peak = l
    return binary_search(time, peak + 1, time - 1, dst, False) - binary_search(time, 0, peak, dst, True) + 1


with open("inputs/input_6.txt") as f:
    times, dist = parse(f.read().splitlines())

print(f"Part 1: {margin(times, dist)}")
print(f"Part 2: {single_race(times, dist)}")
