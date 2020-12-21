from typing import Tuple, Optional


class Rule:
    def match(self, line: str) -> Tuple[bool, Optional[str]]:
        pass


class CharacterMatch(Rule):
    def __init__(self, value: str):
        self.value = value

    def match(self, line: str) -> Tuple[bool, Optional[str]]:
        # print(f'[{self}]: {line} -> ', end='')
        if not line:
            # print('✘')
            return False, None

        head, *tail = line
        if head == self.value:
            line = "".join(tail)
            # print('✔︎')
            return True, line
        else:
            # print('✘')
            return False, None

    def __repr__(self):
        return self.value


class ListRule(Rule):
    def __init__(self, *rule: Rule):
        self.rules = rule

    def match(self, line: str) -> Tuple[bool, Optional[str]]:
        for rule in self.rules:
            matches, line = rule.match(line)
            if not matches:
                return False, None

        return True, line

    def __repr__(self):
        return "".join(f'{rule}' for rule in self.rules)


class OrRule(Rule):
    def __init__(self, *rule: Rule):
        self.rules = rule

    def match(self, line: str) -> Tuple[bool, Optional[str]]:
        for rule in self.rules:
            matches, _line = rule.match(line)
            if matches:
                return True, _line

        return False, None

    def __repr__(self):
        return "(" + \
               "|".join(f'{rule}' for rule in self.rules) + \
               ")"


if __name__ == '__main__':
    a = CharacterMatch('a')
    p = CharacterMatch('p')
    l = CharacterMatch('l')

    e = CharacterMatch('e')

    appl_or_pe = OrRule(ListRule(a, ListRule(p, p), l), ListRule(p, e))

    print(appl_or_pe.match('appl'))
