import ioaoc
import collections

test_input = """2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
1 + 2 * 3 + 4 * 5 + 6"""



def tokenize(line):
    tokens = collections.deque()
    for token in line.split(" "):
        if token in ("+", "*"): 
            tokens.append(token)
            continue

        if token.startswith("("):
            while token.startswith("("):
                tokens.append(token[0])
                token = token[1:]
            tokens.append(int(token))
            continue

        if token.endswith(")"):
            subtokens = []
            while token.endswith(")"):
                subtokens.append(token[-1])
                token = token[:-1]
            subtokens.append(int(token))
            tokens.extend(reversed(subtokens))
            continue
        tokens.append(int(token))

    return tokens

def parse(line):
    tokens = tokenize(line)

    stack = collections.deque()
    rpn = collections.deque()

    while tokens:
        token = tokens.popleft()
        if token == ")":
            while True:
                token = stack.pop()
                if token == "(":
                    break
                rpn.append(token)
        elif token == "(":
            stack.append(token)
        elif token in ("+", "*"):
            if stack and stack[-1] != "(":
                rpn.append(stack.pop())
            stack.append(token)
        else:
            rpn.append(token)

    while stack:
        rpn.append(stack.pop())
    return rpn


def parse2(line):
    tokens = tokenize(line)

    stack = collections.deque()
    rpn = collections.deque()

    while tokens:
        token = tokens.popleft()
        if token == ")":
            while True:
                token = stack.pop()
                if token == "(":
                    break
                rpn.append(token)
        elif token == "(":
            stack.append(token)
        elif token in ("+", "*"):
            while stack and stack[-1] == "+":
                rpn.append(stack.pop())
            stack.append(token)
        elif token == "+":
            if stack and stack[-1] != "(":
                rpn.append(stack.pop())
            stack.append(token)
        else:
            rpn.append(token)

    while stack:
        rpn.append(stack.pop())
    return rpn


def compute(rpn):
    stack = []
    while rpn:
        token = rpn.popleft()
        if token == "*":
            stack.append(stack.pop() * stack.pop())
        elif token == "+":
            stack.append(stack.pop() + stack.pop())
        else:
            stack.append(token)

    [result] = stack
    return result


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day18_input.txt")

    summed = 0
    for line in lines:
        rpn = parse(line)
        result = compute(rpn)
        summed += result

    print(">", summed)

    summed = 0
    for line in lines:
        rpn = parse2(line)
        result = compute(rpn)
        summed += result

    print(">>", summed)
