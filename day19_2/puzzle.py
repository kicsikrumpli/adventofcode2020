from typing import Optional, Iterator


class Rule:
    def match(self, line: str) -> Iterator[Optional[str]]:
        pass

    @staticmethod
    def from_dict(rules: dict, rule_str: str = None) -> 'Rule':
        if rule_str is None:
            rule_str: str = rules[0]

        if '"' in rule_str:
            return CharacterMatch(rule_str.strip('"'))
        elif '|' in rule_str:
            or_rules = [
                Rule.from_dict(rules, part.strip())
                for part
                in rule_str.split('|')
            ]
            return OrMatch(*or_rules)
        elif ' ' in rule_str:
            and_rules = [
                Rule.from_dict(rules, part.strip())
                for part
                in rule_str.split(' ')
            ]
            return ListMatch(*and_rules)
        elif rule_str.strip().isnumeric():
            return Rule.from_dict(rules, rules.get(int(rule_str)))
        else:
            print(f'WUT? {rule_str}')


class CharacterMatch(Rule):
    """
    >>> a = CharacterMatch('a')
    >>> [res for res in a.match('apple')]
    ['pple']

    >>> a = CharacterMatch('a')
    >>> [res for res in a.match('a')]
    ['']

    >>> a = CharacterMatch('a')
    >>> [res for res in a.match(None)]
    []

    """
    def __init__(self, value):
        self.value = value

    def match(self, line: str) -> Iterator[Optional[str]]:
        if line is not None and line.startswith(self.value):
            yield line[1:]


class ListMatch(Rule):
    """
    >>> a = CharacterMatch('a')
    >>> p = CharacterMatch('p')
    >>> list_rule = ListMatch(a, p)
    >>> [res for res in list_rule.match('apple')]
    ['ple']

    >>> a = CharacterMatch('a')
    >>> p = CharacterMatch('p')
    >>> list_rule = ListMatch(a, p)
    >>> [res for res in list_rule.match('ap')]
    ['']

    >>> a = CharacterMatch('a')
    >>> p = CharacterMatch('p')
    >>> list_rule = ListMatch(a, p, p)
    >>> [res for res in list_rule.match('ap')]
    []

    """
    def __init__(self, *rule: Rule):
        self.rules = rule

    def match(self, line: str) -> Iterator[Optional[str]]:
        lines = [line]
        for rule in self.rules:
            lines = [
                line
                for line_in in lines
                for line in rule.match(line_in)
                if line is not None
            ]

        for line in lines:
            yield line


class OrMatch(Rule):
    """
    >>> a = CharacterMatch('a')
    >>> p = CharacterMatch('p')
    >>> l = CharacterMatch('l')
    >>> appl = ListMatch(a, p, p, l)
    >>> ap = ListMatch(a, p)
    >>> or_rule = OrMatch(ap, appl)
    >>> [res for res in or_rule.match('apple')]
    ['ple', 'e']

    >>> a = CharacterMatch('a')
    >>> p = CharacterMatch('p')
    >>> l = CharacterMatch('l')
    >>> appl = ListMatch(a, p, p, l)
    >>> ap = ListMatch(a, p)
    >>> or_rule = OrMatch(ap, appl)
    >>> [res for res in or_rule.match('appl')]
    ['pl', '']

    >>> a = CharacterMatch('a')
    >>> p = CharacterMatch('p')
    >>> l = CharacterMatch('l')
    >>> appl = ListMatch(a, p, p, l)
    >>> ap = ListMatch(a, p)
    >>> or_rule = OrMatch(ap, appl)
    >>> [res for res in or_rule.match('a')]
    []
    """
    def __init__(self, *rule: Rule):
        self.rules = rule

    def match(self, line: str) -> Iterator[Optional[str]]:
        for rule in self.rules:
            for res in rule.match(line):
                if res is not None:
                    yield res


if __name__ == '__main__':
    import doctest
    doctest.testmod()

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

    rule = Rule.from_dict(rules)
    count = 0
    for _input in inputs:
        print(_input, ":", end='')
        matches = [r for r in rule.match(_input)]
        is_match = '' in matches
        count += is_match
        print(is_match, matches)

    print('Total matches:', count)

