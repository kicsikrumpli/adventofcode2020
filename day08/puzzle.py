from enum import Enum
from typing import Tuple


class Op(Enum):
    acc = 'acc'
    jmp = 'jmp'
    nop = 'nop'


def parse_line(line: str) -> Tuple[Op, int]:
    """
    >>> parse_line("nop 42")
    (Op.nop, 42)

    :param line:
    :return:
    """
    op, arg = line.split()
    return Enum[op], int(arg)


if __name__ == '__main__':
    pass