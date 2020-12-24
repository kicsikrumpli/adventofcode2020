from functools import reduce
from pprint import pprint
from typing import List, Iterator

from day20.tile import Tile


def tiles_iter(file) -> Iterator[List[str]]:
    batch = []
    for line in file:
        line: str = line.strip()
        if not line:
            yield batch
            batch = []
        else:
            batch.append(line)
    yield batch


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    with open('input.txt', 'rt') as puzzle:
        tiles = [
            Tile.from_text(lines)
            for lines
            in tiles_iter(puzzle)
        ]

    matches = dict([
        (tile.tile_no, [
            match
            for match in [
                tile.match(other)
                for other
                in tiles
                if other != tile
            ]
            if match
        ])
        for tile in tiles
    ])
    corners = [
        (tile_no, neighbours)
        for tile_no, neighbours
        in matches.items()
        if len(neighbours) == 2
    ]
    pprint(corners)

    corner_ids = [
        tile_no
        for tile_no, _
        in corners
    ]

    # product_of_corner_ids = reduce(lambda a, b: a*b, corner_ids)
    # print(f'product of corner piece id-s: {product_of_corner_ids}')
