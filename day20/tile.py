import itertools
from pprint import pprint
from typing import List, Tuple, Optional


class Tile:
    def __init__(self,
                 tile_no: int,
                 edges: List[str],
                 inside: List[str] = None):
        self.tile_no = tile_no
        # top, right, bottom, left
        self.edges = edges
        self._inside = inside
        self.rotations = 0
        self.flips = 0

    def __repr__(self):
        return f'{self.tile_no}: {self.edges}'

    @property
    def inside(self):
        for _ in range(self.flips % 2):
            self._inside = self._flip_inside()
        for _ in range(self.rotations % 4):
            self._inside = self._rotate_inside()
        self.flips = 0
        self.rotations = 0
        return self._inside

    @staticmethod
    def from_text(lines: List[str]) -> 'Tile':
        """
        >>> tile = Tile.from_text(["Tile 1:",
        ...                        "abcd",
        ...                        "l12e",
        ...                        "k43f",
        ...                        "jihg"])
        >>> pprint(tile)
        1: ['abcd', 'defg', 'ghij', 'jkla']

        >>> tile.inside
        ['12', '43']

        :param lines:
        :return:
        """
        title, *lines = lines
        tile_no = int(title.replace('Tile ', '').replace(':', ''))

        # sides clock_wise, starting from top
        top = lines[0]
        right = "".join(line[-1] for line in lines)
        bottom = lines[-1][-1::-1]
        left = "".join(line[0] for line in lines[-1::-1])

        return Tile(tile_no,
                    [top, right, bottom, left],  # edges
                    [line[1:-1] for line in lines[1:-1]])  # inside

    def flip_horiz(self):
        """
        Flips tile horizontally.
        vertical flip == flip + rotate
        >>> tile = Tile.from_text(["Tile 1:",
        ...                 "abcd",
        ...                 "l12e",
        ...                 "k43f",
        ...                 "jihg"]).flip_horiz()
        >>> tile.edges
        ['dcba', 'alkj', 'jihg', 'gfed']

        >>> tile.inside
        ['21', '34']

        """
        top, right, bottom, left = self.edges
        left, right = right[-1::-1], left[-1::-1]
        top = top[-1::-1]
        bottom = bottom[-1::-1]
        self.edges = [top, right, bottom, left]
        self.flips += 1
        # self._flip_inside()
        return self

    def rotate_cw(self):
        """
        Rotate clockwise 90

        >>> tile = Tile.from_text(["Tile 1:",
        ...                 "abcd",
        ...                 "l12e",
        ...                 "k43f",
        ...                 "jihg"]).rotate_cw()
        >>> tile.edges
        ['jkla', 'abcd', 'defg', 'ghij']

        >>> tile.inside
        ['41', '32']
        """
        top, right, bottom, left = self.edges
        top, right, bottom, left = left, top, right, bottom
        self.edges = [top, right, bottom, left]
        # self._rotate_inside()
        self.rotations += 1
        return self

    def match(self, other: 'Tile') -> Optional[Tuple[int, 'Tile']]:
        """
        Transform _other_ tile to match one side.

        >>> this = Tile.from_text(["Tile 1:",
        ...                        "abcd",
        ...                        "l..e",
        ...                        "k..f",
        ...                        "jihg"])
        >>> other = Tile.from_text(["Tile 2:",
        ...                         "axxx",
        ...                         "l..x",
        ...                         "k..x",
        ...                         "jxxx"])
        >>> this.match(other)
        (3, 2: ['xxxa', 'alkj', 'jxxx', 'xxxx'])

        >>> this = Tile.from_text([
        ...      "Tile 1951:",
        ...      "#.##...##.",
        ...      "#.####...#",
        ...      ".....#..##",
        ...      "#...######",
        ...      ".##.#....#",
        ...      ".###.#####",
        ...      "###.##.##.",
        ...      ".###....#.",
        ...      "..#.#..#.#",
        ...      "#...##.#..",])
        >>> other = Tile.from_text([
        ...      "Tile 2729:",
        ...      "...#.#.#.#",
        ...      "####.#....",
        ...      "..#.#.....",
        ...      "....#..#.#",
        ...      ".##..##.#.",
        ...      ".#.####...",
        ...      "####.#.#..",
        ...      "##.####...",
        ...      "##..#.##..",
        ...      "#.##...##.",])
        >>> this.match(other)
        (0, 2729: ['...#.#.#.#', '#..#......', '.##...##.#', '####....#.'])

                                                      ^
        _this_ matched on top (0) --------------------|

        :param other: rotate / flip, match
        :return: Tuple of
            - index of matched side of (this) tile
            - other tile rotated / flipped to match
        """

        for flips in range(2):
            other.flip_horiz()
            # print(self)
            # print(other)
            # print('=' * 10)
            for edge_index, edge in enumerate(self.edges):
                # print(f'[{edge_index}] {edge} :')
                for rotations in range(4):
                    other.rotate_cw()
                    # opposite side: top <-> bottom, left <-> right
                    other_edge = other.edges[(edge_index + 2) % 4]
                    # print(f'  /{(edge_index + 2) % 4}/ {other_edge[-1::-1]}')
                    if edge == other_edge[-1::-1]:
                        # print('✔︎')
                        return edge_index, other
                # print('-' * 10)
        return None

    def _rotate_inside(self) -> List[str]:
        rows = len(self._inside)

        def _rotate(row, col):
            _row, _col = -col, row
            return _row + rows - 1, _col

        def _get(coords):
            row, col = coords
            return self._inside[row][col]

        return [
            "".join([_get(_rotate(row, col)) for col, _ in enumerate(r)])
            for row, r in enumerate(self._inside)
        ]

    def _flip_inside(self) -> List[str]:
        return [
            line[-1::-1] for line in self._inside
        ]


def rotate(image: List[str]) -> List[str]:
    """
    >>> rotate(["123",
    ...         "456",
    ...         "789"])
    ['741', '852', '963']

    >>> rotate(["1234",
    ...         "5678",
    ...         "90ab",
    ...         "cdef"])
    ['c951', 'd062', 'ea73', 'fb84']

    :return:
    """
    rows = len(image)

    def _rotate(row, col):
        _row, _col = -col, row
        return _row + rows - 1, _col

    def _get(coords):
        row, col = coords
        return image[row][col]

    return [
        "".join([_get(_rotate(row, col)) for col, _ in enumerate(r)])
        for row, r in enumerate(image)
    ]


def flip(image: List[str]) -> List[str]:
    """
    flip horizontally
    >>> flip(["1234",
    ...       "5678",
    ...       "90ab",
    ...       "cdef"])
    ['4321', '8765', 'ba09', 'fedc']

    """
    return [
        line[-1::-1] for line in image
    ]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    pass
