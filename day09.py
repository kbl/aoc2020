import ioaoc

test_input = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


def parse(lines):
    return [int(line) for line in lines]


if __name__ == "__main__":
    buffer = []

    preambule_length = 25
    lines = ioaoc.read_file("day09_input.txt")
    numbers = parse(lines)

    for index_a, number_a in enumerate(numbers[:preambule_length]):
        for index_b, number_b in enumerate(numbers[:preambule_length]):
            if index_a == index_b:
                continue
            buffer.append(number_a + number_b)

    invalid_xmas_number = None
    for index, number in enumerate(numbers):
        if index < preambule_length:
            continue
        if number not in buffer:
            invalid_xmas_number = number
            break
        buffer = buffer[preambule_length:]
        for new_number in numbers[index-preambule_length:index]:
            buffer.append(number + new_number)

    print(">", invalid_xmas_number)

    temporary_sum = 0
    summed_numbers = []
    for index, number in enumerate(numbers):
        while temporary_sum > invalid_xmas_number:
            temporary_sum -= summed_numbers[0]
            summed_numbers = summed_numbers[1:]

        if temporary_sum == invalid_xmas_number:
            break

        summed_numbers.append(number)
        temporary_sum += number

    print(">>", min(summed_numbers) + max(summed_numbers))
