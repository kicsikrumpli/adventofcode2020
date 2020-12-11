from pprint import pprint
from typing import List, Callable


def adjacent_seats(seats: List[List[str]], row: int, col: int) -> int:
    """
    Count number of adjacent seats.
    adjacent is one left, right, up, down, and one on diagonals.
    >>> adjacent_seats([
    ...        ['#', '#', '#'],
    ...        ['#', '#', '#'],
    ...        ['#', '#', '#'],
    ...        ], 1, 1)
    8

    >>> adjacent_seats([
    ...        ['#', '#', '#'],
    ...        ['#', '#', '#'],
    ...        ['#', '#', '#'],
    ...        ], 0, 0)
    3

    >>> adjacent_seats([
    ...        ['#', '#', '#'],
    ...        ['#', '#', '#'],
    ...        ['#', '#', '#'],
    ...        ], 2, 2)
    3

    >>> adjacent_seats([
    ...        ['#', '#', '#'],
    ...        ['#', '.', '#'],
    ...        ['#', '#', '.'],
    ...        ], 2, 2)
    2
    """
    return sum([
        1
        for r in range(max(row - 1, 0), min(row + 2, len(seats)))
        for c in range(max(col - 1, 0), min(col + 2, len(seats[0])))
        if (r, c) != (row, col) and seats[r][c] == '#'
    ])


def apply_rule(kind: str, occupied_adjecent: int, tolerance: int = 4):
    """
    Apply rules to a space.

    >>> apply_rule('.', 0)
    '.'

    >>> apply_rule('L', 0)
    '#'

    >>> apply_rule('L', 1)
    'L'

    >>> apply_rule('#', 4)
    'L'

    >>> apply_rule('#', 3)
    '#'

    :param kind: one of
        '.': no seat
        'L': empty seat
        '#': occupied seat
    :param occupied_adjecent: number of occupied
    :param tolerance: min number of occupied seats it takes to free up a seat
    :return: new space
    """
    if kind == '.':
        return '.'
    elif kind == 'L' and occupied_adjecent == 0:
        return '#'
    elif kind == '#' and occupied_adjecent >= tolerance:
        return 'L'
    else:
        return kind


def step(seats: List[List[str]],
         adjacent: Callable[[List[List[str]], int, int], int] = adjacent_seats,
         tolerance: int = 4,
         ) -> List[List[str]]:
    """
    Change all the seats.

    >>> pprint(step(parse([
    ...     "L.LL.LL.LL\\n",
    ...     "LLLLLLL.LL\\n",
    ...     "L.L.L..L..\\n",
    ...     "LLLL.LL.LL\\n",
    ...     "L.LL.LL.LL\\n",
    ...     "L.LLLLL.LL\\n",
    ...     "..L.L.....\\n",
    ...     "LLLLLLLLLL\\n",
    ...     "L.LLLLLL.L\\n",
    ...     "L.LLLLL.LL"])))
    [['#', '.', '#', '#', '.', '#', '#', '.', '#', '#'],
     ['#', '#', '#', '#', '#', '#', '#', '.', '#', '#'],
     ['#', '.', '#', '.', '#', '.', '.', '#', '.', '.'],
     ['#', '#', '#', '#', '.', '#', '#', '.', '#', '#'],
     ['#', '.', '#', '#', '.', '#', '#', '.', '#', '#'],
     ['#', '.', '#', '#', '#', '#', '#', '.', '#', '#'],
     ['.', '.', '#', '.', '#', '.', '.', '.', '.', '.'],
     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
     ['#', '.', '#', '#', '#', '#', '#', '#', '.', '#'],
     ['#', '.', '#', '#', '#', '#', '#', '.', '#', '#']]

    >>> pprint(step(step(parse([
    ...     "L.LL.LL.LL\\n",
    ...     "LLLLLLL.LL\\n",
    ...     "L.L.L..L..\\n",
    ...     "LLLL.LL.LL\\n",
    ...     "L.LL.LL.LL\\n",
    ...     "L.LLLLL.LL\\n",
    ...     "..L.L.....\\n",
    ...     "LLLLLLLLLL\\n",
    ...     "L.LLLLLL.L\\n",
    ...     "L.LLLLL.LL"]))))
    [['#', '.', 'L', 'L', '.', 'L', '#', '.', '#', '#'],
     ['#', 'L', 'L', 'L', 'L', 'L', 'L', '.', 'L', '#'],
     ['L', '.', 'L', '.', 'L', '.', '.', 'L', '.', '.'],
     ['#', 'L', 'L', 'L', '.', 'L', 'L', '.', 'L', '#'],
     ['#', '.', 'L', 'L', '.', 'L', 'L', '.', 'L', 'L'],
     ['#', '.', 'L', 'L', 'L', 'L', '#', '.', '#', '#'],
     ['.', '.', 'L', '.', 'L', '.', '.', '.', '.', '.'],
     ['#', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', '#'],
     ['#', '.', 'L', 'L', 'L', 'L', 'L', 'L', '.', 'L'],
     ['#', '.', '#', 'L', 'L', 'L', 'L', '.', '#', '#']]

    :param seats: as list of lists
        '.' no seat
        'L' empty seat
        '#' occupied seat
    :param adjacent: function to calculate number of adjacent seats
    :param tolerance: max number of occupied seats to consider for rule
    :return: new seat arrangement after applying rules
    """
    return [
        [
            apply_rule(kind, adjacent(seats, r, c), tolerance)
            for c, kind in enumerate(row)
        ]
        for r, row in enumerate(seats)
    ]


def parse(file):
    """
    >>> pprint(parse([
    ...        "L.LL.LL.LL\\n",
    ...        "LLLLLLL.LL\\n",
    ...        "L.L.L..L..\\n",
    ...        "LLLL.LL.LL\\n",
    ...        "L.LL.LL.LL\\n",
    ...        "L.LLLLL.LL\\n",
    ...        "..L.L.....\\n",
    ...        "LLLLLLLLLL\\n",
    ...        "L.LLLLLL.L\\n",
    ...        "L.LLLLL.LL\\n",
    ...        ]))
    [['L', '.', 'L', 'L', '.', 'L', 'L', '.', 'L', 'L'],
     ['L', 'L', 'L', 'L', 'L', 'L', 'L', '.', 'L', 'L'],
     ['L', '.', 'L', '.', 'L', '.', '.', 'L', '.', '.'],
     ['L', 'L', 'L', 'L', '.', 'L', 'L', '.', 'L', 'L'],
     ['L', '.', 'L', 'L', '.', 'L', 'L', '.', 'L', 'L'],
     ['L', '.', 'L', 'L', 'L', 'L', 'L', '.', 'L', 'L'],
     ['.', '.', 'L', '.', 'L', '.', '.', '.', '.', '.'],
     ['L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L'],
     ['L', '.', 'L', 'L', 'L', 'L', 'L', 'L', '.', 'L'],
     ['L', '.', 'L', 'L', 'L', 'L', 'L', '.', 'L', 'L']]

    """
    return [
        [space for space in row.strip()]
        for row in file
    ]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        seats = parse(puzzle)

    rounds = 1
    while True:
        new_seats = step(seats)
        if new_seats == seats:
            break
        else:
            rounds += 1
            print('.', end='')
            seats = new_seats

    print('-')
    occupied_seats = sum([
        sum([1 for space in row if space == '#'])
        for row in new_seats
    ])
    print(f'number of occupied_seats after {rounds} rounds: {occupied_seats}')
