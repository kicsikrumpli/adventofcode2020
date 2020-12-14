from io import StringIO
from typing import List, Tuple

from day13.modulo import multiplicative_inverse


def transform_bus_ids(line: str):
    return [
        (int(bus_id), offset)
        for offset, bus_id
        in enumerate(line.strip().split(','))
        if bus_id.isnumeric()
    ]


def parse(puzzle) -> List[Tuple[int, int]]:
    """
    parse input text

    >>> parse(StringIO("123\\n1,2,x,3,x"))
    [(1, 0), (2, 1), (3, 3)]

    :param puzzle: file like object with input
    :return: list of bus ids and their indices
    """
    puzzle.readline()
    return transform_bus_ids(puzzle.readline())


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        bus_ids = parse(puzzle)

    """
    What is the earliest timestamp such that 
    all of the listed bus IDs depart at offsets matching their positions in the list?
    """

    # system of congruences
    # bus_ids = transform_bus_ids('7,13,x,x,59,x,31,19')
    # expected_t = 1068781

    print('solve system of congruences:')
    for idx, (bus_id, offset) in enumerate(bus_ids):
        print(f'{idx}.\tt === {(bus_id - offset) % bus_id} (mod {bus_id})')
    print('=' * 10)

    bus_id, offset = bus_ids[0]
    remainder = (bus_id - offset) % bus_id
    modulus = bus_id
    left_side = (modulus, remainder)
    for bus_id, offset in bus_ids[1:]:
        remainder = (bus_id - offset) % bus_id
        modulus = bus_id
        print(f't === {remainder} (mod {modulus})')
        print(f't == {left_side[0]} * k + {left_side[1]}')
        print(f'{left_side[0]} * k + {left_side[1]} === {remainder} (mod {modulus})')
        right_side = (remainder - left_side[1]) % modulus
        print(f'{left_side[0]} * k === {right_side} (mod {modulus})')
        left_inv = multiplicative_inverse(left_side[0], modulus)
        print(f'{left_inv} * {left_side[0]} * k === {left_inv} * {right_side} (mod {modulus})')
        one = (left_inv * left_side[0]) % modulus
        right = (left_inv * right_side) % modulus
        print(f'{one} * k === {right} (mod {modulus})')
        print(f'k == l * {modulus} + {right}')
        print(f't == {left_side[0]} * (l * {modulus} + {right}) + {left_side[1]}')
        left_side = (left_side[0] * modulus, left_side[0] * right + left_side[1])
        print(f't == {left_side[0]} * l + {left_side[1]}')
        print('-' * 10)

    t = left_side[1]
    print('found:', t)
