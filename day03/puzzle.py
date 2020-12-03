from functools import reduce
from typing import Tuple, List


def slope(dx: int, dy: int, max_y: int):
    x = 0
    y = 0
    yield x, y
    while y < max_y - dy:
        x = x + dx
        y = y + dy
        yield x, y


def wrap_around_map(_map: List[str], tree_symbol: str = '#'):
    row_length = len(_map[0])

    def _is_tree_at(x: int, y: int):
        return _map[y][x % row_length] == tree_symbol

    return _is_tree_at


if __name__ == '__main__':
    # dx, dy
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]

    with open('input.txt', 'rt') as puzzle:
        _map = [
            line.strip()
            for line in puzzle
        ]

    is_tree_at = wrap_around_map(_map)

    trees = [
        sum([
            1
            for x, y in slope(dx, dy, len(_map))
            if is_tree_at(x, y)
        ])
        for dx, dy
        in slopes
    ]

    print('slopes: ', slopes)
    print('trees: ', trees)
    print('* of trees', reduce(lambda x, y: x * y, trees))
