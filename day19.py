import ioaoc
import collections
import re

test_input = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""


def parse(lines):
    raw_rules = {}
    messages = []
    for line in lines:
        if not line:
            continue

        tokens = line.split(" ")
        if len(tokens) == 1:
            messages.append(tokens[0])
            continue

        rule_id = int(tokens[0][:-1])
        tokens = tokens[1:]
        if len(tokens) == 1 and '"' in tokens[0]:
            characters = tokens[0][1:-1]
            tokens = [characters]
        elif "|" in tokens:
            split_tokens = []
            current_list_of_tokens = []
            for token in tokens:
                if token == "|":
                    split_tokens.append(current_list_of_tokens)
                    current_list_of_tokens = []
                    continue
                current_list_of_tokens.append(int(token))
            split_tokens.append(current_list_of_tokens)
            tokens = split_tokens
        else:
            tokens = [[int(token) for token in tokens]]

        raw_rules[rule_id] = tokens

    return raw_rules, messages

def is_expanded(rule_set):
    """
    >>> is_expanded([["a"]])
    True
    >>> is_expanded([["a", 1]])
    False
    >>> is_expanded([["abc"], ["a", 1]])
    False
    >>> is_expanded([["abc"], ["acd"]])
    True
    """
    for rule in rule_set:
        if all(isinstance(token, str) for token in rule):
            continue
        return False
    return True

def normalize(rule_set):
    """
    >>> normalize([[]])
    deque([deque([])])
    >>> normalize([[1, 2, "a", "b", 3, "a", "b", "c"]])
    deque([deque([1, 2, 'ab', 3, 'abc'])])
    >>> normalize([[1, 2, "a", "b", 3, "a", "b", "c"], ["a", "b", 3, "a", "b", "c"]])
    deque([deque([1, 2, 'ab', 3, 'abc']), deque(['ab', 3, 'abc'])])
    """
    new_rule_set = collections.deque()
    for rule in rule_set:
        new_rule = collections.deque()
        new_token = ""
        for token in rule:
            if isinstance(token, str):
                new_token += token
                continue
            if new_token:
                new_rule.append(new_token)
                new_token = ""
            new_rule.append(token)
        if new_token:
            new_rule.append(new_token)
        new_rule_set.append(new_rule)

    return new_rule_set

def expand_rule(rule_set, replace_id, replace_rule_set):
    """
    >>> expand_rule([[1, 2, "a"], [2, 2, "b"]], 2, [[3, 4, "c"]])
    deque([deque([1, 3, 4, 'ca']), deque([3, 4, 'c', 3, 4, 'cb'])])
    >>> expand_rule([[2, "a", 2], [2, "b", 2]], 2, [[1, "c"], [3, "d"]])
    deque([deque([1, 'ca', 1, 'c']), deque([3, 'da', 1, 'c']), deque([1, 'ca', 3, 'd']), deque([3, 'da', 3, 'd']), deque([1, 'cb', 1, 'c']), deque([3, 'db', 1, 'c']), deque([1, 'cb', 3, 'd']), deque([3, 'db', 3, 'd'])])
    >>> expand_rule([[2, 2]], 2, [["a", 1, "b"], ["c", 3, "d"], ["e", 4, "f"]])
    deque([deque(['a', 1, 'ba', 1, 'b']), deque(['c', 3, 'da', 1, 'b']), deque(['e', 4, 'fa', 1, 'b']), deque(['a', 1, 'bc', 3, 'd']), deque(['c', 3, 'dc', 3, 'd']), deque(['e', 4, 'fc', 3, 'd']), deque(['a', 1, 'be', 4, 'f']), deque(['c', 3, 'de', 4, 'f']), deque(['e', 4, 'fe', 4, 'f'])])
    """
    new_rule_set = collections.deque()
    for rule in rule_set:
        new_rules = collections.deque()
        new_rules.append(collections.deque())
        for token in rule:
            if token != replace_id:
                for sub_rule in new_rules:
                    sub_rule.append(token)
                continue
            temp_new_rules = collections.deque()
            for replace_rule in replace_rule_set:
                for sub_rule in new_rules:
                    sub_rule = collections.deque(sub_rule)
                    sub_rule.extend(replace_rule)
                    temp_new_rules.append(sub_rule)
            new_rules = temp_new_rules
        new_rule_set.extend(new_rules)

    return normalize(new_rule_set)

def rules_to_expand(rule_set):
    """
    >>> rules_to_expand([[1, 2, 2], ["a", 3, 2]])
    {1, 2, 3}
    """
    to_expand = set()
    for rule in rule_set:
        for token in rule:
            if isinstance(token, str):
                continue
            to_expand.add(token)
    return to_expand


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day19_input.txt")

    raw_rules, messages = parse(lines)
    to_check = sorted(list(raw_rules.keys()))

    i = 0

    while to_check:
        for rule_id, rule_set in sorted(raw_rules.items()):
            print("   ", rule_id, len(rule_set))

        print("iteration", i, len(to_check))

        i += 1

        for rule_id in to_check:
            print("checking", rule_id)
            rule_set = raw_rules[rule_id]
            if is_expanded(rule_set):
                to_check.remove(rule_id)
                continue

            for ri in rules_to_expand(rule_set):
                print(" expanding", ri)
                rule_set = expand_rule(rule_set, ri, raw_rules[ri])
            raw_rules[rule_id] = rule_set

    valid_messages = []

    for rule in raw_rules[0]:
        [rule] = rule
        valid_messages.append(rule)
    
    print(">", len(set(valid_messages).intersection(set(messages))))
