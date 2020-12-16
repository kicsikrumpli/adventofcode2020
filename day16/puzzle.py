from typing import Dict, Tuple, List


def parse(file):
    _constraints: Dict[str, List[Tuple[int, int]]] = dict()
    _my_ticket: List[int] = list()
    _other_tickets: List[List[int]] = list()

    while True:
        line = file.readline().strip()
        if not line:
            break
        else:
            name, consts = line.split(':')
            consts = [
                tuple(int(t) for t in part.split('-'))
                for part
                in consts.strip().split('or')
            ]
            _constraints[name] = consts

    while True:
        line = file.readline().strip()
        if not line:
            break
        elif line == 'your ticket:':
            continue
        else:
            _my_ticket = [int(i) for i in line.split(',')]

    while True:
        line = file.readline().strip()
        if not line:
            break
        elif line == 'nearby tickets:':
            continue
        else:
            _other_tickets.append([int(i) for i in line.split(',')])

    return _constraints, _my_ticket, _other_tickets


def invalid_fields(constraints: Dict[str, List[Tuple[int, int]]], ticket: List[int]) -> List[int]:
    """
    Find fields that are invalid for all of the ranges.

    >>> invalid_fields({'a': [(1, 3), (5, 7)], 'b': [(11, 13), (15, 17)]}, [4, 14])
    [4, 14]

    >>> invalid_fields({'a': [(1, 3), (5, 7)], 'b': [(11, 13), (15, 17)]}, [3, 14])
    [14]

    :param constraints: valid ranges as parsed from input
        label: list of min - max range (inclusive)
    :param ticket: list of values as parsed from input
    :return: True, if no number in ticket is valid
    """
    all_ranges = [
        range(_min, _max + 1)
        for rs in constraints.values()
        for _min, _max in rs
    ]
    return [
        n for n in ticket
        if all(
            n not in r
            for r in all_ranges
        )
    ]


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        constraints, my_ticket, other_tickets = parse(puzzle)

    scaning_error = sum([
        sum(invalid_fields(constraints, ticket))
        for ticket in other_tickets
    ])

    print('ticket scanning error rate for nearby tickets:', scaning_error)
