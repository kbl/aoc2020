import ioaoc


def binary_search(lower, upper, instructions):
    while instructions:
        index = (lower + upper) // 2

        if instructions[0] in ("L", "F"):
            upper = index
        else:
            lower = index + 1

        instructions = instructions[1:]
    return lower


def seat_id(identifier):
    return binary_search(0, 127, identifier[0:7]) * 8 + binary_search(0, 7, identifier[7:])


if __name__ == "__main__":
    lines = ioaoc.read_file("day05_input.txt")
    seats = sorted([seat_id(seat) for seat in lines])

    print(">", max(seats))

    for lower, upper in zip(seats[:-1], seats[1:]):
        if lower + 1 == upper -1:
            print(">>", lower + 1)

