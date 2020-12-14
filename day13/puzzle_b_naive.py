import itertools
import math
from math import lcm
from typing import List, Tuple
from io import StringIO


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
            id0 = 3
    t       D
    t+1     .
    t+2     .
    t+3     D
    t+4     .
    t+5     .
    t+6     D
    t+7     .
    """

    # naive
    bus_ids = transform_bus_ids('7,13,x,x,59,x,31,19')
    # bus_ids = transform_bus_ids('7,13')
    print(bus_ids)
    timestamps = (
        t
        for t in itertools.count()
        if all(
            (t + offset) % bus_id == 0
            for bus_id, offset
            in bus_ids
        )
    )
    t = next(timestamps)
    print(t)
    print('expected:', 1068781)
    print([(bus_id - t) % bus_id for bus_id, _ in bus_ids])
    print([t + offset for _, offset in bus_ids])

