import ioaoc


if __name__ == "__main__":
    lines = ioaoc.read_file("day01_input.txt")
    numbers = [int(line) for line in lines]

    tripple_sum = set()
    for index_x, x in enumerate(numbers):
        for index_y, y in enumerate(numbers[index_x:]):

            if x + y == 2020:
                print(">", x*y)

            for z in numbers[index_y:]:
                if x + y + z == 2020:
                    print(">>", x*y*z)
