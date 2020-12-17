from functools import reduce
from pprint import pprint
from typing import Dict, Tuple, List, Set


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


def is_valid_ticket(constraints, ticket) -> bool:
    return not invalid_fields(constraints, ticket)


def all_valid_tickets(constraints, tickets) -> List[List[int]]:
    return [
        ticket
        for ticket in other_tickets
        if is_valid_ticket(constraints, ticket)
    ]


def possible_labels(constraints: Dict[str, List[Tuple[int, int]]],
                    ticket: List[int],
                    # allowed_fields: List[Set[str]],
                    ) -> List[Set[str]]:
    """
    For every field in the ticket list all the possible labels for which it is valid.

    x>>> resp = possible_labels(
    ...     {'a': [(1, 3), (5, 7)], 'b': [(11, 13), (0, 10)], 'c': [(0, 100)]},
    ...     [2, 12],
    ...     [{'a'}, {'b', 'c'}]
    ...     )
    x>>> [sorted(list(s)) for s in resp]
    [['a'], ['b', 'c']]

    :param constraints: as parsed from input
    :param ticket: as parsed from input
    :return: list of sets of possible field labels
    """

    # return [
    #     {
    #         label
    #         for label, ranges in constraints.items()
    #         if label in allowed and
    #            any(
    #                field_value in range(_min, _max + 1)
    #                for _min, _max in ranges
    #            )
    #     }
    #     for field_value, allowed in zip(ticket, allowed_fields)
    # ]


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        constraints, my_ticket, other_tickets = parse(puzzle)

    # part 1.
    scaning_error = sum([
        sum(invalid_fields(constraints, ticket))
        for ticket in other_tickets
    ])
    print('ticket scanning error rate for nearby tickets:', scaning_error)

    # part 2.
    valid_tickets = all_valid_tickets(constraints, other_tickets)
    """    
    all possible field ids for a label
    if for all the tickets
    field is within any of the valid ranges
    """
    possible_fields = {
        label: [
            field_id
            for field_id, _ in enumerate(my_ticket)
            if all(
                    any(
                        ticket[field_id] in range(_min, _max + 1)
                        for _min, _max in ranges
                    )
                    for ticket in valid_tickets
            )
        ]
        for label, ranges in constraints.items()
    }

    """
    possible fields are in increasing lengths
    {
      'class': [2, 4, 19],
      'duration': [2, 3, 4, 19],
      'price': [0, 2, 3, 4, 19],
      'seat': [2, 19],
      'train': [2],
    }
    for each field pick the number from possible numbers
    that is not in any of the other lists that are shorter in length
    seat: pick 19, b/c 19 not in [2]
    class pick 4, b/c 4 not in [2], [2, 19]
    """
    field_ids = {
        label: [
            field for field in fields
            if all(
                field not in other_fields
                for other_fields in possible_fields.values()
                if len(other_fields) < len(fields)
            )
        ][-1]  # every one should be of length 1
        for label, fields in possible_fields.items()
    }

    """
    Once you work out which field is which, 
    look for the six fields on your ticket that start with the word departure. 
    What do you get if you multiply those six values together
    """
    departure_values = [
        my_ticket[field_id]
        for label, field_id in field_ids.items()
        if label.startswith('departure')
    ]
    product = reduce(lambda a, b: a*b, departure_values)
    print('Product of "departure" field values:', product)