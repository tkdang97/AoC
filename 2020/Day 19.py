from utils.data import *


def parse(data):
    rules = {}
    rule_list, messages = data.split("\n\n")
    for line in rule_list.splitlines():
        rule_num, rule = line.split(": ")
        if rule[0] == '"':
            rule = rule[1:-1]
        else:
            rule = [seq.split() for seq in rule.split(" | ")]
        rules[rule_num] = rule

    return rules, messages.splitlines()


def test_sequence(rules, sequence, string):
    if not sequence:
        yield string
    else:
        n, *sequence = sequence
        for res_string in test_message(rules, n, string):
            yield from test_sequence(rules, sequence, res_string)
            

def test_alternatives(rules, alternatives, string):
    for sequence in alternatives:
        yield from test_sequence(rules, sequence, string)
        

def test_message(rules, n, string):
    if isinstance(rules[n], list):
        yield from test_alternatives(rules, rules[n], string)
    else:
        if string and string[0] == rules[n]:
            yield string[1:]
            
            
def match(rules, string):
    return any(m == "" for m in test_message(rules, "0", string))


def part1(rules, messages):
    return sum(match(rules, message) for message in messages)


def part2(rules, messages):
    modified_rules = {**rules, '8': [['42'], ['42', '8']], '11': [['42', '31'], ['42', '11', '31']]}
    return sum(match(modified_rules, message) for message in messages)


test = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

data = get_and_write_data(19, 2020)
rules, messages = parse(data)
print_output(part1(rules, messages), part2(rules, messages))
