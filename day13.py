import ioaoc


test_input = """939
7,13,x,x,59,x,31,19"""

test_input = """0
1789,37,47,1889"""

EMPTY = "x"

def parse(lines):
    time = int(lines[0])
    buses = []
    for token in lines[1].split(","):
        if token == EMPTY:
            buses.append(token)
            continue
        buses.append(int(token))
    return time, buses


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day13_input.txt")
    
    time, buses = parse(lines)

    minimum_delay = None
    minimum_bus = None
    for bus in buses:
        if bus == EMPTY:
            continue

        reminder = time % bus
        if reminder == 0:
            minimum_delay = 0 
            minimum_bus = bus
            continue

        delay = bus - reminder
        if minimum_delay is None or delay < minimum_delay:
            minimum_delay = delay
            minimum_bus = bus

    print(">", minimum_delay * minimum_bus)

    buses2 = []
    for index, token in enumerate(buses):
        if token == EMPTY:
            continue
        buses2.append((index, token))

    to_add = buses2[0][1]
    current = 0
    for reminder, number in buses2[1:]:
        while True:
            current += to_add
            if (current + reminder) % number == 0:
                to_add *= number
                break

    print(">>", current)
