import ioaoc
import re

test_input = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

test_input2 = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

def is_valid_byr(value):
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    try:
        value = int(value)
    except ValueError:
        return False
    return 1920 <= value <= 2002

def is_valid_iyr(value):
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    try:
        value = int(value)
    except ValueError:
        return False
    return 2010 <= value <= 2020


def is_valid_eyr(value):
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    try:
        value = int(value)
    except ValueError:
        return False
    return 2020 <= value and value <= 2030


def is_valid_hgt(value):
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    try:
        numeric_value = int(value[:-2])
    except ValueError:
        return False

    if value[-2:] == "cm":
        return 150 <= numeric_value <= 193
    if value[-2:] == "in":
        return 59 <= numeric_value <= 76
    return False


def is_valid_hcl(value):
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    return bool(re.match("^#[0-9a-f]{6}$", value))


def is_valid_ecl(value):
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    valid_colors = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    return value in valid_colors


def is_valid_pid(value):
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    return bool(re.match("^[0-9]{9}$", value))


def is_valid_cid(value):
    # cid (Country ID) - ignored, missing or not.
    return True


validation_rules = {field: globals()[f"is_valid_{field}"] for field in ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid")}


def parse_passport_data(raw):
    fields = dict()
    passports = []
    for line in raw:
        if not line:
            passports.append(fields)
            fields = dict()
            continue
        fields.update([token.split(":") for token in line.split(" ")])

    return passports


FIELD_COUNT = 8

def has_required_fields(passport):
    if len(passport) == (FIELD_COUNT - 1) and "cid" not in passport:
        return True
    return len(passport) == FIELD_COUNT


def has_valid_fields(passport):
    return all([validation_rules[field](value) for field, value in passport.items()])


if __name__ == "__main__":
    lines = test_input2.split("\n")
    lines = ioaoc.read_file("day04_input.txt")
    passports = parse_passport_data(lines)

    valid_passports = [p for p in passports if has_required_fields(p)]
    print(">", len(valid_passports))

    even_more_valid_passports = [p for p in valid_passports if has_valid_fields(p)]
    print(">>", len(even_more_valid_passports))
