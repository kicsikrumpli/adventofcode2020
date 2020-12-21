from typing import Tuple, List

from day18.tokenizer import tokenize, Token, Number, Symbol


def peek(stack: List):
    if stack:
        return stack[-1]
    else:
        return None


def apply(symbol: Symbol, left: int, right: int):
    if symbol is Symbol.Plus:
        return left + right
    if symbol is Symbol.Asterisk:
        return left * right


def eval(tokens: List[Token]) -> int:
    """
    >>> eval(tokenize('1 + 2 * 3 + 4 * 5 + 6'))
    71

    >>> eval(tokenize('1 + (2 * 3) + (4 * (5 + 6))'))
    51

    >>> eval(tokenize('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))
    13632
    """
    def _eval(tokens: List[Token], stack: List = None) -> Tuple:
        if stack is None:
            stack = list()

        if not tokens:
            return stack[-1], tokens

        head, *tokens = tokens

        if head in (Symbol.Asterisk, Symbol.Plus):
            return _eval(tokens, [*stack, head])
        elif head is Symbol.CloseParen:
            return stack[-1], tokens
        elif head is Symbol.OpenParen:
            value, remaining_tokens = _eval(tokens)
            return _eval([Number(value), *remaining_tokens], stack)
        elif isinstance(head, Number):
            if peek(stack) in (Symbol.Asterisk, Symbol.Plus):
                op = stack.pop()
                left = head.value
                right = stack.pop()
                return _eval([Number(apply(op, left, right)), *tokens], stack)
            else:
                return _eval(tokens, [*stack, head.value])

    return _eval(tokens)[0]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        values = [
            eval(tokenize(line.strip()))
            for line
            in puzzle
        ]

    sum_of_values = sum(values)
    print('sum of values:', sum_of_values)