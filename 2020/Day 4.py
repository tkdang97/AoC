from utils.data import *


def parse(data):
    return [passport.split() for passport in data.split("\n\n")]


def part1(passports):
    valid = 0
    for passport in passports:
        if len(passport) == 8:
            valid += 1
        elif len(passport) == 7:
            keys = set()
            for entry in passport:
                key, _ = entry.split(":")
                keys.add(key)
            if "cid" not in keys:
                valid += 1
    return valid


def check_key(key, value):
    match key:
        case "byr":
            return len(value) == 4 and value.isdigit() and 1920 <= int(value) <= 2002
        case "iyr":
            return len(value) == 4 and value.isdigit() and 2010 <= int(value) <= 2020
        case "eyr":
            return len(value) == 4 and value.isdigit() and 2020 <= int(value) <= 2030
        case "hgt":
            if value.endswith("cm"):
                return value[:-2].isdigit() and 150 <= int(value[:-2]) <= 193
            if value.endswith("in"):
                return value[:-2].isdigit() and 59 <= int(value[:-2]) <= 76
        case "hcl":
            return len(value) == 7 and value[0] == "#" and all(val in "0123456789abcdef" for val in value[1:])
        case "ecl":
            return value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
        case "pid":
            return len(value) == 9 and value.isdigit()
        case "cid":
            return True


def part2(passports):
    total_valid = 0
    for passport in passports:
        if len(passport) >= 7:
            keys = set()
            valid = True
            for entry in passport:
                key, value = entry.split(":")
                keys.add(key)
                if not check_key(key, value):
                    valid = False
                    break
            if valid and (len(keys) == 8 or "cid" not in keys):
                total_valid += 1
    return total_valid


test = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

data = get_and_write_data(4, 2020)
passports = parse(data)
print_output(part1(passports), part2(passports))
