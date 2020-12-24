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


def expand(rule_set, expanded_rules, messages):
    """
    >>> list(sorted(expand(["a", ["a", 1], [1, "a"]], {1: {"abb", "bbc"}}, {"aabbabbc", "abbabbca"})))
    ['a', 'aabb', 'abba', 'abbc', 'bbca']
    >>> list(sorted(expand(["a", ["a", 1], [1, "a"], [1, 1]], {1: {"abb", "bbc"}}, {"aabbabbcabbabbbbc", "bbcaaacc"})))
    ['a', 'aabb', 'abba', 'abbabb', 'abbbbc', 'abbc', 'bbca', 'bbcabb']
    >>> list(sorted(expand([[2, 3], [3, 2]], {2: {"aa", "bb"}, 3: {"ab", "ba"}}, {'ababbb', 'bababa', 'abbbab', 'aaabbb', 'aaaabbb'})))
    ['aaab', 'abbb', 'babb', 'bbab', 'bbba']
    >>> sorted([str(x) for x in expand([[1], [1, 1], [1, 2]], {1: ["a", "b"]}, ["aab"])])
    ["('a', 2)", "('b', 2)", 'a', 'aa', 'ab', 'b']
    >>> sorted([str(x) for x in expand([[1, 3], [1, 2, 3]], {1: ["a", "b"], 3: ["a", "b"]}, ["aab"])])
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

            indices_to_remove = set()
            for nested_index, nested_token in enumerate(nested_rule):
                for new_rule_index in range(new_rules_length):
                    index = nested_index * new_rules_length + new_rule_index
                    if new_rules[index] and isinstance(new_rules[index][-1], str) and isinstance(nested_token, str):
                        new_rules[index][-1] += nested_token
                        is_in_messages = any((new_rules[index][-1] in message for message in messages))
                        if not is_in_messages:
                            indices_to_remove.add(index)
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

def expand_recursive(rule_id, rule_set, messages):
    """
    >>> list(sorted(expand_recursive(2, [("a", 2, "a"), ("a", 2, "b"), ("b", 2, "a"), ("b", 2, "b"), "aa", "ab"], ["aaaabbb", "baba"])))
    ['aa', 'aaaa', 'aaaabb', 'aaab', 'aaabbb', 'aabb', 'ab', 'baba']
    """
    tuple_rule_set = []
    for rule in rule_set:
        if isinstance(rule, str):
            rule = (rule, )
        tuple_rule_set.append(rule)

    expanded_rule_set = set()
    rules_to_expand = collections.deque(tuple_rule_set)

    max_length = max([len(message) for message in messages])

    i = 0
    while rules_to_expand:
        i += 1
        rule = rules_to_expand.popleft()

        if i % 100 == 0:
            print(i, "rules", len(rules_to_expand))

        new_rules = [[]]

        for token in rule:
            indices_to_remove = set()
            if isinstance(token, str):
                for index, new_rule in enumerate(new_rules):
                    if new_rule and isinstance(new_rule[-1], str):
                        new_rule[-1] += token
                        is_in_messages = any((message.startswith(new_rule[-1]) or message.endswith(new_rule[-1]) for message in messages))
                        if not is_in_messages:
                            indices_to_remove.add(index)
                    else:
                        new_rule.append(token)
            elif token == rule_id:
                recursive_rule = tuple_rule_set
                new_rules_length = len(new_rules)
                recursive_rule_length = len(recursive_rule)

                for _ in range(recursive_rule_length - 1):
                    for index in range(new_rules_length):
                        new_rules.append(list(new_rules[index]))

                for nested_index, nested_tokens in enumerate(recursive_rule):
                    for nested_token in nested_tokens:
                        for new_rule_index in range(new_rules_length):
                            index = nested_index * new_rules_length + new_rule_index
                            new_rule = new_rules[index]

                            if isinstance(nested_token, str):
                                if new_rule and isinstance(new_rule[-1], str):
                                    new_rule[-1] += nested_token
                                    is_in_messages = any((message.startswith(new_rule[-1]) or message.endswith(new_rule[-1]) for message in messages))
                                    if not is_in_messages:
                                        indices_to_remove.add(index)
                                else:
                                    new_rule.append(nested_token)
                            else:
                                new_rule.append(nested_token)
            else:
                raise ValueError(f"unexpected token {token}")

            for index in sorted(indices_to_remove, reverse=True):
                del new_rules[index]

        x = 0
        for rule in new_rules:
            if len(rule) == 1:
                [rule] = rule
                expanded_rule_set.add(rule)
            else:
                length = 0
                for token in rule:
                    if token == rule_id:
                        length += 1
                    else:
                        length += len(token)

                if length >= max_length:
                    x += 1
                    continue

                rules_to_expand.append(rule)
        if x:
            print(" removed", x)

    return expanded_rule_set


if __name__ == "__main__":
    lines = test_input.split("\n")
    lines = ioaoc.read_file("day19_input.txt")

    raw_rules, messages = parse(lines)
    ordered_rules = order(raw_rules)

    # expanded_rules = {}
    # for rule_id, rule_set in order(raw_rules).items():
    #     expanded_rules[rule_id] = expand(rule_set, expanded_rules, messages)

    # print(">", len(set(expanded_rules[0]).intersection(set(messages))))

    raw_rules[8] = [[42], [42, 8]]
    raw_rules[11] = [[42, 31], [42, 11, 31]]
    ordered_rules = order(raw_rules)

    expanded_rules = {}
    for rule_id, rule_set in order(raw_rules).items():
        print("expanding", rule_id)
        expanded_rule = expand(rule_set, expanded_rules, messages)
        if not all((isinstance(valid, str) for valid in expanded_rule)):
            print("expanding recursive")
            expanded_rules[rule_id] = expand_recursive(rule_id, expanded_rule, messages)
        expanded_rules[rule_id] = expanded_rule
        print(" ", len(expanded_rule))

    print(">>", len(set(expanded_rules[0]).intersection(set(messages))))
