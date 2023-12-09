import re


def get_numbers(s):
    first = last = ""
    for c in s:
        if c.isdigit():
            if first == "":
                first = c
            last = c
    return int(first + last)


def get_modified_numbers(s):
    replace_vals = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
                    "six": "6", "seven": "7", "eight": "8", "nine": "9"}
    modified = s
    for k, v in replace_vals.items():
        modified = re.sub(k, k[0] + v + k[-1], modified)  # need to keep first and last characters to account for overlaps
    print(f"{s.strip()} | {modified.strip()}")
    return get_numbers(modified)


sm = 0
mod_sum = 0
with open("inputs/input_1.txt", "r") as f:
    for i, line in enumerate(f):
        num = get_numbers(line)
        sm += num
        mod_num = get_modified_numbers(line)
        mod_sum += mod_num
        print(f"Line {i + 1}: {mod_num}\n")

print(sm)
print(mod_sum)
