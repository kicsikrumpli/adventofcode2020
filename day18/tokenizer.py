from enum import Enum
from typing import List, Optional, Union


class Token:
    @staticmethod
    def parse(ch: str) -> Optional['Token']:
        if ch.isnumeric():
            return Number(ch)
        elif ch in (s.value for s in Symbol):
            return next(s for s in Symbol if s.value == ch)
        else:
            return None


class Number(Token):
    def __init__(self, value: Union[str, int]):
        self.value: int = int(value)

    def __repr__(self):
        return f'Num({self.value})'


class Symbol(Token, Enum):
    Plus = '+'
    Asterisk = '*'
    OpenParen = '('
    CloseParen = ')'


def tokenize(line: str) -> List[Token]:
    return [
        token
        for token
        in [
            Token.parse(c)
            for c in line
        ]
        if token is not None
    ]
