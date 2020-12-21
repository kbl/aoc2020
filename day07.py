import ioaoc
import dataclasses
import re

test_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""


def parse(lines):
    nodes = dict()

    for line in lines:
        tokens = line.split(" ", 4)
        root_name = " ".join(tokens[:2])
        nodes[root_name] = []

        if tokens[4].startswith("no"):
            continue

        tokens = tokens[4].split(",")
        nested_nodes = []
        for token in tokens:
            token = token.strip()
            nested_tokens = token.split(" ")
            name = " ".join(nested_tokens[1:3])
            count = int(nested_tokens[0])

            nested_nodes.append((name, count))
        nodes[root_name] = nested_nodes

    return nodes


def traverse(needle, to_visit, all_bags, visited):
    while to_visit:
        if needle in to_visit:
            return True

        next_to_check = to_visit.pop()

        names = [name for name, _ in all_bags[next_to_check]]
        to_visit.update(names)

    return False


def bag_count(bag, all_bags):
    nested_bag_count = 0
    for name, count in all_bags[bag]:
        nested_bag_count += count + count * bag_count(name, all_bags)
    return nested_bag_count


NEEDLE = "shiny gold"


if __name__ == "__main__":
    lines = test_input.split("\n")
    all_bags = parse(ioaoc.read_file("day07_input.txt"))

    has_needle = set([NEEDLE])
    visited = set()

    for bag, nested in all_bags.items():
        to_visit = set([name for name, _ in nested])
        if traverse(NEEDLE, to_visit, all_bags, visited):
            has_needle.add(bag)
        visited.add(bag)

    print(">", len(has_needle) - 1)
    print(">>", bag_count(NEEDLE, all_bags))
