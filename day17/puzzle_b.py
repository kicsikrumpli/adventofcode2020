from pprint import pprint
from typing import Tuple, List, Union


def dim(space: Union[List, str]):
    """
    >>> dim('#')
    0

    >>> dim(['#', '#', '#'])
    1

    >>> dim([['#', '#', '#'], ['#', '#', '#']])
    2

    >>> dim([[['#', '#', '#'], ['#', '#', '#']]])
    3

    >>> dim([[[['#', '#', '#'], ['#', '#', '#']]]])
    4
    """
    if isinstance(space, str):
        return 0
    else:
        return 1 + dim(space[0])


def size(space: Union[List, str]) -> Tuple:
    """
    Find size of space for each dimension.

    >>> size('.')
    ()

    >>> size(['.', '.', '.'])
    (3,)

    >>> size(
    ...     [['#', '#', '#'],
    ...      ['#', '#', '#']])
    (2, 3)

    >>> size(default_space((2, 3)))
    (2, 3)

    :param space: to find size of
    :return: tuple
        eg: (z, y, x)
    """
    if isinstance(space, str):
        return tuple()
    else:
        return tuple([len(space), *size(space[0])])


def default_space(size: Tuple) -> Union[str, List]:
    """
    Make default space of size.

    0 dim space
    >>> default_space(tuple())
    '.'

    1 dim space: vector
    >>> default_space((3,))
    ['.', '.', '.']

    2 dim space: plane
    >>> default_space((3, 2))
    [['.', '.'], ['.', '.'], ['.', '.']]

    3 dim space: space
    >>> default_space((1, 2, 2))
    [[['.', '.'], ['.', '.']]]

    4 dim space: hyper-space
    >>> default_space((1,1,3,3))
    [[[['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]]]

    :param size: tuple, size in each dimension,
        e.g.: (z, y, x)
    :return:
    """
    if len(size) == 0:
        return '.'
    else:
        d = size[0]
        tail = size[1:]
        return [
            default_space(tail)
            for _ in range(d)
        ]


def grow_space(space: Union[List, str]) -> Union[List, str]:
    """
    >>> grow_space(['x', 'x'])
    ['.', 'x', 'x', '.']

    >>> pprint(grow_space([['x', 'x'], ['x', 'x']]))
    [['.', '.', '.', '.'],
     ['.', 'x', 'x', '.'],
     ['.', 'x', 'x', '.'],
     ['.', '.', '.', '.']]

    >>> pprint(grow_space([[['x', 'x'], ['x', 'x']]]))
    [[['.', '.', '.', '.'],
      ['.', '.', '.', '.'],
      ['.', '.', '.', '.'],
      ['.', '.', '.', '.']],
     [['.', '.', '.', '.'],
      ['.', 'x', 'x', '.'],
      ['.', 'x', 'x', '.'],
      ['.', '.', '.', '.']],
     [['.', '.', '.', '.'],
      ['.', '.', '.', '.'],
      ['.', '.', '.', '.'],
      ['.', '.', '.', '.']]]


    :param space: to grow
    :return: grown space in each dimension by 1 +/-
    """
    if dim(space) == 0:
        return space
    else:
        pass
        return [
            grow_space(default_space(size(space)[1:])),
            * [
                grow_space(subspace)
                for subspace in space
            ],
            grow_space(default_space(size(space)[1:])),
        ]


def count_active(space: Union[str, List]):
    """
    count active cells in space (denoted by '#').

    >>> count_active('#')
    True

    >>> count_active(['.', '#', '.'])
    1

    >>> count_active([['#', '.'], ['.', '#']])
    2

    >>> count_active([[['#', '.'], ['.', '#']], [['#', '.'], ['.', '.']]])
    3

    :param space:
    :return:
    """
    if isinstance(space, str):
        return space == '#'
    else:
        return sum(
            count_active(subspace)
            for subspace
            in space
        )


def count_active_around(space: Union[str, List], coords: Tuple):
    """
    count active cells around +/- 1 of center,
        including cell at coordinates

    >>> count_active_around([
    ...     ['#', '.', '.', '.', '#'],
    ...     ['.', '#', '.', '.', '.'],
    ...     ['.', '.', '#', '.', '.'],
    ...     ['.', '#', '.', '#', '.'],
    ...     ['.', '.', '#', '.', '.']], (2, 2))
    4

    :param space: to count cells in
    :param coords: center
    :return: number of active cells ('#'-s)
    """
    if isinstance(space, str):
        return space == '#'
    else:
        return sum(
            count_active_around(subspace, coords[1:])
            for subspace
            in space[max(coords[0] - 1, 0): coords[0] + 2]
        )


def transform(cell: str, active_count: int, coords) -> str:
    """
    Transform cell according to conway's rules.

    :param cell: value to transform
    :param active_count: active cells in +/- 1 neighbourhood, including cell
    :return:
    """
    if cell == '#' and active_count in (3, 4):
        return '#'
    elif cell == '.' and active_count == 3:
        return '#'
    else:
        return '.'


def step(space: List):
    def _step(_space: Union[str, List],
              coords: Tuple = None):
        if coords is None:
            coords = tuple()

        if isinstance(_space, str):
            return transform(_space, count_active_around(grown_space, coords), coords)
        else:
            return [
                _step(subspace, (*coords, coord))
                for coord, subspace
                in enumerate(_space)
            ]

    grown_space = grow_space(space)
    return _step(grown_space)


def neighbors(space: List):
    def _neighbors(_space: Union[str, List],
              coords: Tuple = None):
        if coords is None:
            coords = tuple()

        if isinstance(_space, str):
            return f'{coords}: {_space} [{count_active_around(space, coords)}]'
        else:
            return [
                _neighbors(subspace, (*coords, coord))
                for coord, subspace
                in enumerate(_space)
            ]

    return _neighbors(space)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    starting_patch = []
    with open('input.txt', 'rt') as puzzle:
        for line in puzzle:
            starting_patch.append([c for c in line.strip()])

    space = [[starting_patch]]

    print(f'in {dim(space)} dimension space:')

    cycles = 6
    for _ in range(cycles):
        space = step(space)

    print(f'number of active cells after {cycles} cycles:', count_active(space))

