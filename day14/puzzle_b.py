from collections import defaultdict
from pprint import pprint
from typing import Dict, Optional, Generator, List


def substitutions(s: str, substs: Dict[str, str] = None) -> List[str]:
    """
    Substitute characters in s from substitution dictionary.
    If a character is mapped to multiple charecters, all possible substitutions are returned.
    If a character is not in substitution dict, it is left the same

    >>> substitutions('0101')
    ['0101']

    >>> substitutions('010X')
    ['0100', '0101']

    >>> substitutions('X10X')
    ['0100', '0101', '1100', '1101']

    >>> substitutions('0101', {'0': '1', '1': '0'})
    ['1010']

    >>> substitutions('010X', {'0': '1', 'X': '01'})
    ['1110', '1111']

    :param s: string to make substitutions in
    :param substs: substitutions dict
    :return: all possible substitutions
    """
    if not substs:
        substs = {
            'X': '01',
            '1': '1',
            '0': '0'
        }
    if not s:
        return ['']

    vocab = substs.get(s[0], s[0])
    return [
        "".join([digit, *rest])
        for digit in vocab
        for rest in substitutions(s[1:], substs)
    ]


def mem_mask(bitmask: str, num: int) -> List[int]:
    """
    Apply bitmask to num.

    >>> for b in mem_mask('111000', 0b101010):
    ...     format(b, '06b')
    '111010'

    >>> for b in mem_mask('11100X', 0b101010):
    ...     format(b, '06b')
    '111010'
    '111011'

    >>> for b in mem_mask('0X0XX', 0b11010):
    ...     format(b, '06b')
    '010000'
    '010001'
    '010010'
    '010011'
    '011000'
    '011001'
    '011010'
    '011011'

    :param bitmask:
        'X': floating, return values both where this bit is 0 and 1
        '1': set bit to 1
        '0': leave bit unchanged
    :param num: number to mask
    :return: masked number
    """
    floating_masks = [int(s, 2) for s in substitutions(bitmask, {'X': '01', '0': '1'})]
    set_masks = [int(s, 2) for s in substitutions(bitmask, {'X': '01'})]
    return [(num & floating_mask) | set_mask for floating_mask, set_mask in zip(floating_masks, set_masks)]


def mem_generator() -> Generator[None, Optional[str], Dict[int, int]]:
    """

    >>> mem = mem_generator()
    >>> mem.send('mask = 000000000000000000000000000000X1001X')
    >>> mem.send('mem[42] = 100')
    >>> mem.send('mask = 00000000000000000000000000000000X0XX')
    >>> mem.send('mem[26] = 1')
    >>> try:
    ...     mem.send(None)
    ... except StopIteration as e:
    ...     pprint(e.value)
    {16: 1, 17: 1, 18: 1, 19: 1, 24: 1, 25: 1, 26: 1, 27: 1, 58: 100, 59: 100}

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
                for _addr in mem_mask(bitmask, int(addr)):
                    mem[_addr] = int(value)

        return dict(mem)

    gen = _generator()
    next(gen)
    return gen


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    mem = mem_generator()
    with open('input.txt', 'rt') as puzzle:
        pass
        for line in puzzle:
            mem.send(line)

    try:
        mem.send(None)
    except StopIteration as e:
        dump: Dict[int, int] = e.value
        print('sum of all numbers in memory:', sum(dump.values()))

