import ioaoc
import collections

test_input = """16
10
15
5
1
11
7
19
6
12
4"""


def parse(lines):
    numbers = list(sorted([int(number) for number in lines]))
    numbers = [0] + numbers + [numbers[-1]+3]
    return numbers


if __name__ == "__main__":
    lines = ioaoc.read_file("day10_input.txt")
    numbers = parse(lines)

    previous = 0
    jumps = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
    }
    for number in numbers:
        jumps[number - previous]+=1
        previous = number                 

    print(">", jumps[1] * jumps[3])

    possibilities = 0
    last_numbers = [numbers[1]]

    ways_to_achieve = {0: 1}

    for index, number in enumerate(numbers):
        if index + 1 >= len(numbers):
            continue
        next_number = numbers[index + 1]
        if next_number - number > 3:
            continue
        ways_to_achieve[next_number] = ways_to_achieve.get(next_number, 0) + ways_to_achieve[number]

        if index + 2 >= len(numbers):
            continue
        next_number = numbers[index + 2]
        if next_number - number > 3:
            continue
        ways_to_achieve[next_number] = ways_to_achieve.get(next_number, 0) + ways_to_achieve[number]

        if index + 3 >= len(numbers):
            continue
        next_number = numbers[index + 3]
        if next_number - number > 3:
            continue
        ways_to_achieve[next_number] = ways_to_achieve.get(next_number, 0) + ways_to_achieve[number]

    print(">>", ways_to_achieve[numbers[-1]])
