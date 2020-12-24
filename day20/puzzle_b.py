from typing import List, Set, Tuple, Optional, Any

from day20.puzzle import tiles_iter
from day20.tile import Tile, rotate, flip


def place(board: List[List[Optional[Tile]]],
          unplaced: Set[Tile],
          find_neighbors: List[Tuple[int, int]]):

    # direction from find_neighbor to relative row, col coordinates
    directions = {
        0: (-1, 0),  # up
        1: (0, 1),  # right
        2: (1, 0),  # down
        3: (0, -1)  # left
    }

    if not find_neighbors:
        return board

    row, col = find_neighbors.pop()
    neighbors = [
        neighbour
        for neighbour
        in (board[row][col].match(other) for other in unplaced)
        if neighbour
    ]
    for i, neighbour in neighbors:
        r, c = directions[i]
        _row, _col = row + r, col + c
        board[_row][_col] = neighbour
        unplaced.remove(neighbour)
        find_neighbors.append((_row, _col))

    return place(board, unplaced, find_neighbors)


def crop(_board: List[List[Any]]):
    return [
        [tile for tile in row if tile]
        for row in _board
        if any(row)
    ]


def make_image(_board: List[List[Tile]]):
    tile_height = len(_board[0][0].inside)
    image = []
    for row in board:
        for line_i in range(tile_height):
            # line = "|". join([
            line = "".join([
                tile.inside[line_i]
                for tile in row
            ])
            image.append(line)
        # image.append("-" * len(line))
    return image


def find_serpent_in_image(image: List[str],
                          serpent: List[str]):
    im_w = len(image[0])
    serp_w = len(serpent[0])
    # turn image into a vector,
    image_as_str = "".join(image)
    # turn serpent into a vector, pad with whitespace, so that each line lines up
    serpent_as_str = "".join(line + " " * (im_w - serp_w) for line in serpent)

    for image_index, _ in enumerate(image_as_str):
        for serpent_index, serpent_char in enumerate(serpent_as_str):
            if image_index + serpent_index >= len(image_as_str):
                # not enough space left for a full serpent
                break
            if serpent_char != ' ' and serpent_char != image_as_str[image_index + serpent_index]:
                # no match
                break
        else:
            # all charecters in the serpent matched
            yield image_index


if __name__ == '__main__':
    with open('input.txt', 'rt') as puzzle:
        tiles = [
            Tile.from_text(lines)
            for lines
            in tiles_iter(puzzle)
        ]

    # board is 12 x 12 tiles
    width = 24
    height = 24
    board: List[List[Optional[Tile]]] = [
        [None for _ in range(width)]
        for _ in range(height)
    ]
    row, col = width // 2, height // 2

    unplaced: Set[Tile] = set(tiles)
    board[row][col] = unplaced.pop()
    board = place(board=board, unplaced=unplaced, find_neighbors=[(row, col)])

    board = crop(board)
    image = make_image(board)

    serpent = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]

    found_indices = []
    # try all rotations and flips!
    for _ in range(2):
        for _ in range(4):
            image = rotate(image)
            found_indices = [i for i in find_serpent_in_image(image, serpent)]
            if found_indices:
                break
        else:
            image = flip(image)
            continue
        break

    hashmarks_in_image = sum([
        c == '#'
        for row in image
        for c in row
    ])
    hashmarks_in_serpent = sum([
        c == '#'
        for row in serpent
        for c in row
    ])
    number_of_serpents = len(found_indices)
    print(f'hashmarks not in serpents: {hashmarks_in_image - hashmarks_in_serpent * number_of_serpents}')

