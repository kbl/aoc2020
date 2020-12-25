import ioaoc

test_input = """5764801
17807724"""

MAGIC = 20201227

def parse(lines):
    key_public_key, door_public_key = lines
    return int(key_public_key), int(door_public_key)


def loop_size(subject_number, public_key):
    value = 1
    iteration = 0
    while value != public_key:
        iteration += 1
        value *= subject_number
        value %= MAGIC

    return iteration, value


def transform(loop, key):
    value = 1
    for _ in range(loop):
        value *= key
        value %= MAGIC
    return value


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day25_input.txt")

    key, door = parse(lines)
    key_loop, value = loop_size(7, key)
    print(">", transform(key_loop, door))
