from typing import Tuple, List, Union

from day18.tokenizer import tokenize, Token, Number, Symbol


def peek(stack: List):
    if stack:
        return stack[-1]
    else:
        return None


def apply(symbol: Symbol, left: Number, right: Number):
    if symbol is Symbol.Plus:
        return Number(left.value + right.value)
    if symbol is Symbol.Asterisk:
        return Number(left.value * right.value)


def rewrite(tokens: List[Token]):
    """
    >>> rewrite(tokenize('1 + 2 * 3 + 4 * 5 + 6'))
    231

    >>> rewrite(tokenize('1 + (2 * 3) + 4 * 5 + 6'))
    121

    >>> rewrite(tokenize('1 + (2 * 3) + (4 * (5 + 6))'))
    51

    >>> rewrite(tokenize('2 * 3 + (4 * 5)'))
    46

    >>> rewrite(tokenize('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    1445

    >>> rewrite(tokenize('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    669060

    >>> rewrite(tokenize('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))
    23340
    """
    def do_rewrite(tokens: List[Token],
                   operator_stack: List[Symbol] = None,
                   number_stack: List[Number] = None):

        high_precedence_ops = (Symbol.Plus, )  # advent of code silly math
        low_precedence_ops = (Symbol.Asterisk, )

        # print(f'tokens: {tokens}')
        # print(f'operator_stack: {operator_stack}')
        # print(f'number_stack: {number_stack}')
        # print('-' * 10)

        if operator_stack is None:
            operator_stack = list()
        if number_stack is None:
            number_stack = list()

        if not tokens:
            if operator_stack:
                # out of tokens, lets process stack
                *operator_stack, op = operator_stack
                left, right, *number_stack = number_stack
                val = apply(op, left, right)
                number_stack = [*number_stack, val]
                return do_rewrite(tokens, operator_stack, number_stack)
            else:
                return tokens, operator_stack, number_stack

        token, *tokens = tokens
        if isinstance(token, Number):
            number_stack = [*number_stack, token]
            if peek(operator_stack) in high_precedence_ops:
                *operator_stack, op = operator_stack
                *number_stack, left, right = number_stack
                val = apply(op, left, right)
                tokens = [val, *tokens]  # put rewritten high precedence op back as token
        elif token is Symbol.Plus:
            operator_stack = [*operator_stack, token]
        elif token is Symbol.Asterisk:
            operator_stack = [*operator_stack, token]
        elif token is Symbol.OpenParen:
            # print('> OPEN (')
            _tokens, _, _number_stack = do_rewrite(tokens, [], [])  # rewrite expression in parens
            tokens = [*_number_stack, *_tokens]  # put rewritten parenthesis back as token
            # print('< OPEN (')
        elif token is Symbol.CloseParen:
            # print('> CLOSE )')
            _tokens = tokens  # consumed tokens until close paren
            _, _, _number_stack = do_rewrite([], operator_stack, number_stack)  # force processing of stack
            # print('< CLOSE )')
            return tokens, _, _number_stack  # send remaining tokens and stack result back to open paren
        else:
            pass

        return do_rewrite(tokens, operator_stack, number_stack)

    (_, _, (val, *_)) = do_rewrite(tokens)
    return val.value


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        results = [
            rewrite(tokenize(line))
            for line
            in puzzle
        ]

    print('sum of results:', sum(results))
