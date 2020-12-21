import ioaoc
import itertools

test_input = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

test_input = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""


def parse(lines):
    def parse_field(line):
        name, ranges = line.split(":")
        range1, _, range2 = ranges[1:].split(" ")
        range1 = [int(token) for token in range1.split("-")]
        range2 = [int(token) for token in range2.split("-")]
        return name, [range1, range2]

    def parse_ticket(line):
        return [int(token) for token in line.split(",")]

    TICKET_FIELDS = 0
    YOUR_TICKET = 1
    NEARBY_TICKETS = 2

    line_type = TICKET_FIELDS

    fields = []
    your_ticket = None
    nearby_tickets = []
     
    for line in lines:
        if not line:
            continue
        if line == "your ticket:":
            line_type = YOUR_TICKET
            continue
        if line == "nearby tickets:":
            line_type = NEARBY_TICKETS
            continue

        if line_type == TICKET_FIELDS:
            fields.append(parse_field(line))
        if line_type == YOUR_TICKET:
            your_ticket = parse_ticket(line)
        if line_type == NEARBY_TICKETS:
            nearby_tickets.append(parse_ticket(line))

    return fields, your_ticket, nearby_tickets


def is_within_range(value, ranges):
    for min_value, max_value in ranges:
        if value >= min_value and value <= max_value:
            return True

    return False


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day16_input.txt")

    fields, your_ticket, nearby_tickets = parse(lines)

    all_ranges = list(itertools.chain(*[ranges for _, ranges in fields]))

    invalid_fields = []
    for ticket in nearby_tickets:
        for field in ticket:
            if not is_within_range(field, all_ranges):
                invalid_fields.append(field)

    print(">", sum(invalid_fields))

    valid_tickets = []
    for ticket in nearby_tickets:
        if all([is_within_range(field, all_ranges) for field in ticket]):
            valid_tickets.append(ticket)

    potential_field_names = {}

    for ticket in valid_tickets: 
        for field_index, field in enumerate(ticket):
            potential_names = set()
            for name, ranges in fields:
                if is_within_range(field, ranges):
                    potential_names.add(name)
            existing_potential_names = potential_field_names.get(field_index, potential_names)
            potential_field_names[field_index] = existing_potential_names.intersection(potential_names)

    field_indices = {}
    while potential_field_names:
        for field_index, potential_names in potential_field_names.items():
            if len(potential_names) == 1:
                [name] = potential_names
                field_indices[name] = field_index

        for name in field_indices:
            keys_to_remove = []
            for key, potential_names in potential_field_names.items():
                if name in potential_names:
                    potential_names.remove(name)
                if not potential_names:
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                del potential_field_names[key]

    field_multiplication = 1
    for key, index in field_indices.items():
        if key.startswith("departure"):
            field_multiplication *= your_ticket[index]

    print(">>", field_multiplication)
