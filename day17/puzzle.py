from enum import Enum
from pprint import pprint
from typing import List


class States(Enum):
    ACTIVE = '#'
    INACTIVE = '.'


def grow_row(row: List[str],
             default: str = States.INACTIVE.value) -> List[str]:
    """
    Grow a single row by one on the two ends.

    >>> grow_row(['x', 'x', 'x'])
    ['.', 'x', 'x', 'x', '.']

    >>> grow_row([])
    ['.', '.']

    :param row: to grow on the sides by one
    :param default: value to grow with
    :return: grown row
    """
    return [default, *row, default]


def default_row(size: int,
                default: str = States.INACTIVE.value) -> List[str]:
    """
    Create a row of defaut values.

    >>> default_row(0)
    []

    >>> default_row(3)
    ['.', '.', '.']

    :param size: size of row
    :param default: value to fill row with
    :return: row of default values
    """
    return [default for _ in range(size)]


def grow_patch(patch: List[List[str]],
               default: str = States.INACTIVE.value) -> List[List[str]]:
    """
    Grow a patch row and column-wise by one.

    >>> pprint(grow_patch([['x', 'x', 'x'], ['x', 'x', 'x'], ['x', 'x', 'x']]))
    [['.', '.', '.', '.', '.'],
     ['.', 'x', 'x', 'x', '.'],
     ['.', 'x', 'x', 'x', '.'],
     ['.', 'x', 'x', 'x', '.'],
     ['.', '.', '.', '.', '.']]

    :param patch: to grow
    :param default: value to grow with
    :return: grown patch
    """
    return [
        grow_row(default_row(len(patch[0]), default), default),
        *[
            grow_row(row, default)
            for row
            in patch
        ],
        grow_row(default_row(len(patch[0]), default), default),
    ]


def default_patch(rows: int, cols: int,
                  default: str = States.INACTIVE.value) -> List[List[str]]:
    """
    Create a patch of default values.

    >>> default_patch(2, 3)
    [['.', '.', '.'], ['.', '.', '.']]

    :param rows: number of rows
    :param cols: number of columns
    :param default: value to fill patch with
    :return: new patch
    """
    return [
        default_row(cols, default)
        for _ in range(rows)
    ]


def grow_space(space: List[List[List[str]]],
               default: str = States.INACTIVE.value) -> List[List[List[str]]]:
    """
    Grow a space by one depth, row, col in both directions.

    >>> pprint(grow_space([default_patch(3, 3, 'x')]))
    [[['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.']],
     [['.', '.', '.', '.', '.'],
      ['.', 'x', 'x', 'x', '.'],
      ['.', 'x', 'x', 'x', '.'],
      ['.', 'x', 'x', 'x', '.'],
      ['.', '.', '.', '.', '.']],
     [['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.']]]

    :param space: to grow
    :param default: value to grow with
    :return: grown space
    """
    cols = len(space[-1][-1])
    rows = len(space[-1])
    return [
        grow_patch(default_patch(rows, cols, default), default),
        *[
            grow_patch(patch, default)
            for patch
            in space
        ],
        grow_patch(default_patch(rows, cols, default), default)
    ]


def count_neighbors(space: List[List[List[str]]],
                    depth: int,
                    row: int,
                    col: int,
                    value_to_count: str = States.ACTIVE.value) -> int:
    """
    Count neighbors of a point in space by 1 space with value.

    >>> space = grow_space([default_patch(2, 2, 'x')])
    >>> count_neighbors(space, 1, 1, 1, 'x')
    3

    >>> count_neighbors(space, 1, 1, 1, '.')
    23

    >>> space = grow_space([[['O', 'x'], ['x', '-']]])
    >>> count_neighbors(space, 1, 1, 1, 'x')
    2

    :param space: of points
    :param depth: of point to find neighbors of
    :param row: of point to find neighbors of
    :param col: of point to find neighbors of
    :param value_to_count: in neighbors
    :return: number of neighboring values

    """
    max_z = len(space)  # depth
    max_y = len(space[0])  # row
    max_x = len(space[0][0])  # col

    return sum(
        1
        for x in range(max(col - 1, 0), min(col + 2, max_x))
        for y in range(max(row - 1, 0), min(row + 2, max_y))
        for z in range(max(depth - 1, 0), min(depth + 2, max_z))
        if not (x == col and y == row and z == depth) and
            space[z][y][x] == value_to_count
    )


def transform(cell: str, active_neighbors: int) -> str:
    if cell == States.ACTIVE.value and active_neighbors in (2, 3):
        return States.ACTIVE.value
    elif cell == States.INACTIVE.value and active_neighbors == 3:
        return States.ACTIVE.value
    else:
        return States.INACTIVE.value


def step(space: List[List[List[str]]]) -> List[List[List[str]]]:
    """
    Execute one cycle with 3d conway rules (see transform(...)).

    >>> _space = [[['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]]
    >>> pprint(step(_space))
    [[['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.'],
      ['.', '#', '.', '.', '.'],
      ['.', '.', '.', '#', '.'],
      ['.', '.', '#', '.', '.']],
     [['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.'],
      ['.', '#', '.', '#', '.'],
      ['.', '.', '#', '#', '.'],
      ['.', '.', '#', '.', '.']],
     [['.', '.', '.', '.', '.'],
      ['.', '.', '.', '.', '.'],
      ['.', '#', '.', '.', '.'],
      ['.', '.', '.', '#', '.'],
      ['.', '.', '#', '.', '.']]]

    :param space: to cycle
    :return: new space
    """
    _space = grow_space(space)
    return [
        [
            [
                transform(cell, count_neighbors(_space, z, y, x))
                for x, cell in enumerate(row)
            ]
            for y, row in enumerate(patch)
        ]
        for z, patch in enumerate(_space)
    ]


def count_active(space: List[List[List[str]]], active: str = States.ACTIVE.value) -> int:
    """
    Count all active states in space.

    >>> count_active([[['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]])
    5

    :param space: to count active cells in
    :param active: character for active state
    :return: number active cells
    """
    return sum([
        1
        for patch in space
        for row in patch
        for cell in row
        if cell == active
    ])


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    starting_patch = []
    with open('input.txt', 'rt') as puzzle:
        for line in puzzle:
            starting_patch.append([c for c in line.strip()])

    starting_space = [starting_patch]

    cycles = 6
    space = starting_space

    for _ in range(cycles):
        space = step(space)

    print(f'number of active cells after {cycles} cycles:', count_active(space))

