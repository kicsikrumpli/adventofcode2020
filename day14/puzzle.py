from collections import defaultdict
from typing import Dict, Optional, Generator


def mask(bitmask: str, num: int) -> int:
    """
    Apply bitmask to num.

    >>> mask('X'*36, 68719476735)
    68719476735

    >>> mask('X'*36, 0)
    0

    >>> mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 11)
    73

    :param bitmask:
        'X': don't change
        '1': change to 1
        '0': change to 0
    :param num: number to mask
    :return: masked number
    """
    and_mask = int(bitmask.replace('X', '1'), 2)
    or_mask = int(bitmask.replace('X', '0'), 2)
    return (num & and_mask) | or_mask


def mem_generator() -> Generator[None, Optional[str], Dict[int, int]]:
    """
    >>> mem = mem_generator()
    >>> mem.send('mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X')
    >>> mem.send('mem[8] = 11')
    >>> mem.send('mem[7] = 101')
    >>> mem.send('mem[8] = 0')
    >>> try:
    ...     mem.send(None)
    ... except StopIteration as e:
    ...     e.value
    {8: 64, 7: 101}

    """
    def _generator() -> Generator[None, Optional[str], Dict[int, int]]:
        bitmask: str = 'X' * 36
        mem = defaultdict(lambda: 0)

        while True:
            line: str = yield

            if not line:
                break
            elif line.startswith('mask = '):
                bitmask = line.strip().replace('mask = ', '')
            elif line.startswith('mem['):
                addr, value = line.strip()\
                    .replace('mem[', '')\
                    .replace('] = ', '=')\
                    .split('=')
                mem[int(addr)] = mask(bitmask, int(value))

        return dict(mem)

    gen = _generator()
    next(gen)
    return gen


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    mem = mem_generator()
    with open('input.txt', 'rt') as puzzle:
        for line in puzzle:
            mem.send(line)

    try:
        mem.send(None)
    except StopIteration as e:
        dump: Dict[int, int] = e.value
        print('sum of all numbers in memory:', sum(dump.values()))

