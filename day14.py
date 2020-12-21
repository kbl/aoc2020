import ioaoc


test_input = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

MASK = "MASK"
MEMORY = "MEM"


def parse(lines):
    parsed = []
    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" ")[2]
            parsed.append((MASK, (mask, )))
            continue
        
        register, _, value = line.split(" ")
        register = int(register[4:-1])
        value = int(value)
        parsed.append((MEMORY, (register, value)))
    return parsed


def parse_mask(mask):
    or_mask = int(mask.replace("X", "0"), 2)
    and_mask = int(mask.replace("X", "1"), 2)
    return or_mask, and_mask


def mask_addresses(mask, value):
    or_mask = int(mask.replace("X", "0"), 2)
    value |= or_mask
    value = bin(value)[2:].zfill(36)

    addresses = []

    x_count = mask.count("X")
    for submask in range(2**x_count):
        submask = list(bin(submask)[2:].zfill(x_count))
        
        modified_value = []
        for bit, mask_bit in zip(value, mask):
            if mask_bit == "X":
                bit = submask.pop()
            modified_value.append(bit)

        addresses.append(int("".join(modified_value), 2))

    return addresses


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day14_input.txt")
    parsed = parse(lines)

    memory = {}
    for line_type, tokens in parsed:
        if line_type == MASK:
            [mask] = tokens
            or_mask, and_mask = parse_mask(mask)
            continue

        register, value = tokens
        
        value |= or_mask
        value &= and_mask

        memory[register] = value

    s = sum(memory.values())
    print(">", sum(memory.values()))

    memory2 = {}
    for line_type, tokens in parsed:
        if line_type == MASK:
            [mask] = tokens
            continue

        register, value = tokens

        for masked_register in mask_addresses(mask, register):
            memory2[masked_register] = value

    print(">>", sum(memory2.values()))
