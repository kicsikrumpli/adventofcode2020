from day19.rules import Rule, CharacterMatch, OrRule, ListRule


def parse_rule(rules: dict, rule_str: str = None) -> Rule:
    if rule_str is None:
        rule_str: str = rules[0]

    if '"' in rule_str:
        return CharacterMatch(rule_str.strip('"'))
    elif '|' in rule_str:
        or_rules = [
            parse_rule(rules, part.strip())
            for part
            in rule_str.split('|')
        ]
        return OrRule(*or_rules)
    elif ' ' in rule_str:
        and_rules = [
            parse_rule(rules, part.strip())
            for part
            in rule_str.split(' ')
        ]
        return ListRule(*and_rules)
    elif rule_str.strip().isnumeric():
        return parse_rule(rules, rules.get(int(rule_str)))
    else:
        print(f'WUT? {rule_str}')


if __name__ == '__main__':
    with open('input.txt', 'rt') as puzzle:
        rules = dict()
        while True:
            line = puzzle.readline().strip()
            if not line:
                break
            number, rule = line.split(': ')
            rules[int(number)] = rule

        inputs = []
        while True:
            line = puzzle.readline().strip()
            if not line:
                break
            inputs.append(line)

    rule = parse_rule(rules)
    matches = sum([
        is_match
        for is_match, left
        in [
            rule.match(_input)
            for _input
            in inputs
        ]
        if not left
    ])

    print(f'number of matching messages: {matches}')
