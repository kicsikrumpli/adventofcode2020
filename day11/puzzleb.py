from typing import List, Any, Set, Optional, Generator, Iterator

from day11.puzzle import parse, step


def project_direction(mtx: List[List[str]],
                      row: int,
                      col: int,
                      row_step: int,
                      col_step: int) -> Iterator[str]:
    """
    Generator to return elements of a matrix from a starting point in a direction.

    >>> for n in project_direction([
    ...        [' 1', ' 2', ' 3', ' 4', ' 5'],
    ...        [' 6', ' 7', ' 0', ' 9', '10'],
    ...        ['11', '12', '13', '14', '15'],
    ...        ['16', '17', '18', '19', '20']
    ...        ], 1, 2, 1, 1):
    ...     print(n)
    14
    20

    :param mtx: to project from
    :param row: starting row
    :param col: starting col
    :param row_step: row index increment for next element
    :param col_step: column index increment for next element
    :return: generator that returns elements in the direction of (row_step, col_step)
        generator does not return starting element
    """
    row = row + row_step
    col = col + col_step
    while 0 <= row < len(mtx) and 0 <= col < len(mtx[0]):
        yield mtx[row][col]
        row = row + row_step
        col = col + col_step


def first_in_dir(mtx: List[List[str]],
                 row: int,
                 col: int,
                 row_step: int,
                 col_step: int,
                 vocabulary: Set[str] = None,
                 default_value: str = 'X',) -> Optional[str]:
    """
    >>> first_in_dir([['1','0','0','0','2']], 0, 0, 0, 1, {'2'})
    '2'

    >>> first_in_dir([['1','0','0','0','1']], 0, 0, 0, 1, {'2'})
    'X'

    """
    if vocabulary is None:
        vocabulary = {'#', 'L'}

    try:
        return next(elem
                    for elem
                    in project_direction(mtx, row, col, row_step, col_step)
                    if elem in vocabulary)
    except StopIteration as e:
        return default_value


def queen_seats(seats: List[List[Any]],
                row: int,
                col: int) -> int:
    """
    Number of occupied seats in chess_queen directions from a space.
    In every direction we can only see to the first seat, occupied or empty.

    >>> queen_seats([
    ...        ['#', '.', '.', '.', '#'],
    ...        ['.', 'L', '.', '.', '.'],
    ...        ['L', '.', 'L', '.', 'L'],
    ...        ['.', '.', '.', '.', '.'],
    ...        ['#', '.', '.', '.', '#'],
    ...        ], 2, 2)
    3

    :param seats: mtx of all the seats
        '.': no seat
        '#': occupied
        'L': empty
    :param row: row index of seat
    :param col: col index of seat
    :return: number of occupied seats
    """
    directions = [
        (i, j)
        for i in range(-1, 2)
        for j in range(-1, 2)
        if not ((i == 0) and (j == 0))
    ]

    return sum([
        {'L': 0, '#': 1}.get(first_in_dir(seats, row, col, row_step, col_step), 0)
        for row_step, col_step in directions
        if seats[row][col] in {'L', '#'}
    ])


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        seats = parse(puzzle)

    rounds = 1
    while True:
        new_seats = step(seats, queen_seats, 5)
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
