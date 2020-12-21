import ioaoc

def parse(lines):
    groups = []
    group = []
    for line in lines:
        if not line:
            groups.append(group)
            group = []
            continue
        group.add(line)
    groups.append(group)
    return groups


def parse(lines):
    groups = []
    group = []
    for line in lines:
        if not line:
            groups.append(group)
            group = []
            continue

        group.append(line)
    groups.append(group)
    return groups

if __name__ == "__main__":
    lines = ioaoc.read_file("day06_input.txt")
    groups = parse(lines)

    unique_answers = 0
    for group in groups:
        group_unique_answers = set()
        for answers in group:
            group_unique_answers.update(answers)
        unique_answers += len(group_unique_answers)

    print(">", unique_answers)

    total_yes = 0
    for group in groups:
        all_yes = set(group[0])
        for answers in group[1:]:
            all_yes.intersection_update(set(answers))
        total_yes += len(all_yes)

    print(">>", total_yes)
