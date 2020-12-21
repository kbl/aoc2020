def read_file(path):
    with open(path) as input_file:
        return [line.strip() for line in input_file.readlines()]
