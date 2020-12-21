import collections
import ioaoc


def parse(lines):
    parsed_lines = []
    for line in lines:
        password_policy, letter, password = line.split(" ")
        letter = letter[0]
        lowest, highest = [int(number) for number in password_policy.split("-")]
        parsed_lines.append(((lowest, highest), letter, password))

    return parsed_lines

if __name__ == "__main__":
    lines = ioaoc.read_file("day02_input.txt")
    parsed_lines = parse(lines)

    valid = []
    for (lowest, highest), letter, password in parsed_lines:
        password = collections.Counter(password)
        if password[letter] >= lowest and password[letter] <= highest:
            valid.append(password)

    print(">", len(valid))

    valid = []
    for (lowest, highest), letter, password in parsed_lines:
        occurences = 0
        if password[lowest - 1] == letter:
            occurences += 1
        if password[highest - 1] == letter:
            occurences += 1

        if occurences == 1:
            valid.append(password)

    print(">>", len(valid))
