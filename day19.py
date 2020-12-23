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


def order(rule_set):
    """
    >>> order({3: [[4, 5], [2]], 5: ["b"], 1: [[2, 3]], 2: [[4, 4], [5, 5]], 4: ["a"], 0: [[4, 1, 5]]})
    OrderedDict([(5, ['b']), (4, ['a']), (2, [[4, 4], [5, 5]]), (3, [[4, 5], [2]]), (1, [[2, 3]]), (0, [[4, 1, 5]])])
    >>> order({3: [[4, 3, 5], [2]], 5: ["b"], 1: [[2, 3]], 2: [[4, 4], [5, 5]], 4: ["a"], 0: [[4, 1, 5]]})
    OrderedDict([(5, ['b']), (4, ['a']), (2, [[4, 4], [5, 5]]), (3, [[4, 3, 5], [2]]), (1, [[2, 3]]), (0, [[4, 1, 5]])])
    """
    ordered_rule_set = collections.OrderedDict()

    ordered = set()
    dependencies = {}
    
    for rule_id, rules in rule_set.items():
        depends_on = set()
        for rule in rules:
            for token in rule:
                is_shallow_cicle = token == rule_id
                if token in rule_set and not is_shallow_cicle:
                    depends_on.add(token)
        dependencies[rule_id] = depends_on
    
    rules_to_check = collections.deque(dependencies.keys())
    while rules_to_check:
        rule_id = rules_to_check.popleft()
        rule_dependencies = dependencies[rule_id]
        if not rule_dependencies:
            ordered.add(rule_id)
            ordered_rule_set[rule_id] = rule_set[rule_id]
            for rule_id, rule_dependencies in dependencies.items():
                dependencies[rule_id] -= ordered
        else:
            rules_to_check.append(rule_id)

    return ordered_rule_set


def is_recursive(rule_id, rule_set):
    """
    >>> is_recursive(2, ["abc", [1, 3]])
    False
    >>> is_recursive(2, ["abc", [1, 2, 3]])
    True
    """
    for rule in rule_set:
        if isinstance(rule, str):
            continue
        if rule_id in rule:
            return True
    return False


def expand_recursive(rule_set, expanded_rules, messages):
    """
    >>> list(sorted(expand_recursive(["a", ["a", 1], [1, "a"]], {1: {"abb", "bbc"}}, {"aabbabbc", "abbabbca"})))
    ['a', 'aabb', 'abba', 'abbc', 'bbca']
    >>> list(sorted(expand_recursive(["a", ["a", 1], [1, "a"], [1, 1]], {1: {"abb", "bbc"}}, {"aabbabbcabbabbbbc", "bbcaaacc"})))
    ['a', 'aabb', 'abba', 'abbabb', 'abbbbc', 'abbc', 'bbca', 'bbcabb']
    >>> list(sorted(expand_recursive([[2, 3], [3, 2]], {2: {"aa", "bb"}, 3: {"ab", "ba"}}, {'ababbb', 'bababa', 'abbbab', 'aaabbb', 'aaaabbb'})))
    ['aaab', 'abbb', 'babb', 'bbab', 'bbba']
    >>> sorted([str(x) for x in expand_recursive([[1], [1, 1], [1, 2]], {1: ["a", "b"]}, ["aab"])])
    ["('a', 2)", "('b', 2)", 'a', 'aa', 'ab', 'b']
    >>> sorted([str(x) for x in expand_recursive([[1, 3], [1, 2, 3]], {1: ["a", "b"], 3: ["a", "b"]}, ["aab"])])
    ["('a', 2, 'a')", "('a', 2, 'b')", "('b', 2, 'a')", "('b', 2, 'b')", 'aa', 'ab']
    """

    expanded_rule_set = set()
    for rule in rule_set:
        if isinstance(rule, str):
            expanded_rule_set.add(rule)
            continue

        new_rules = [[]]
        for token in rule:
            nested_rule = expanded_rules.get(token, [token])
            new_rules_length = len(new_rules)
            nested_rule_length = len(nested_rule)

            for _ in range(nested_rule_length - 1):
                for index in range(new_rules_length):
                    new_rules.append(list(new_rules[index]))

            indices_to_remove = []
            for nested_index, nested_token in enumerate(nested_rule):
                for new_rule_index in range(new_rules_length):
                    index = nested_index * new_rules_length + new_rule_index
                    if new_rules[index] and isinstance(new_rules[index][-1], str) and isinstance(nested_token, str):
                        new_rules[index][-1] += nested_token
                        is_in_messages = any((new_rules[index][-1] in message for message in messages))
                        if not is_in_messages:
                            indices_to_remove.append(index)
                    else:
                        new_rules[index].append(nested_token)

            for index in sorted(indices_to_remove, reverse=True):
               del new_rules[index]

        for new_rule in new_rules:
            if len(new_rule) == 1 and isinstance(new_rule[0], str):
                expanded_rule_set.add(new_rule[0])
            else:
                expanded_rule_set.add(tuple(new_rule))

    return expanded_rule_set


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day19_input.txt")

    raw_rules, messages = parse(lines)
    ordered_rules = order(raw_rules)

    expanded_rules = {}
    for rule_id, rule_set in order(raw_rules).items():
        expanded_rules[rule_id] = expand_recursive(rule_set, expanded_rules, messages)

    print(">", len(set(expanded_rules[0]).intersection(set(messages))))

    # raw_rules[8] = [[42], [42, 8]]
    # raw_rules[11] = [[42, 31], [42, 11, 31]]
    # ordered_rules = order(raw_rules)

    # expanded_rules = {}
    # for rule_id, rule_set in order(raw_rules).items():
    #     if is_recursive(rule_id, rule_set):
    #         expanded_rule_set = expand_recursive(rule_id, rule_set, expanded_rules, messages)
    #     else:
    #         expanded_rule_set = expand(rule_set, expanded_rules, messages)
    #     expanded_rules[rule_id] = expanded_rule_set

    # print(">>", len(set(expanded_rules[0]).intersection(set(messages))))
