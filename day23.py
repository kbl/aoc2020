import collections

test_input = """
"""


if __name__ == "__main__":
    line = "389125467"
    line = "643719258"

    cups = collections.deque([int(element) for element in line])
    cups.extend(range(10, 1000001))

    current = 1
    picked = collections.deque()
    LOWEST = min(cups)
    HIGHEST = max(cups)

    print(len(cups))

    i = 0
    moves = 10000000
    seen = {}
    while cups:
        i += 1
        if i > moves:
            break

        if i % 100 == 0:
            print(i)
        current = cups.popleft()
        cups.append(current)

        cup1 = cups.popleft()
        cup2 = cups.popleft()
        cup3 = cups.popleft()

        destination = current
        while True:
            destination -= 1

            if destination < LOWEST:
                destination = HIGHEST

            if destination in (cup1, cup2, cup3):
                continue

            break
        index = cups.index(destination) + 1
        cups.insert(index, cup3)
        cups.insert(index, cup2)
        cups.insert(index, cup1)

    current = cups[-1]
    while current != 1:
        current = cups.popleft()
        cups.append(current)

    print(''.join([str(x) for x in cups][:-1]))

