def decode(s: str):
    """
    decode 7+3 char string as row and col

    >>> decode("FBFBBFFRLR")
    (44, 5)

    >>> decode("BFFFBBFRRR")
    (70, 7)

    >>> decode("FFFBBBFRRR")
    (14, 7)

    >>> decode("BBFFBBFRLL")
    (102, 4)

    :param s: ^[FB]{7}[LR]{3}$
    :return: tuple of row, col
    """
    return row(s[0:7]), col(s[7:])


def row(s: str):
    """
    Decode row from 7 character string by partitioning range from 0 to 127:
        F: front - split, take lower half, eg. 0 - 63
        B: back - split, take upper half, eg. 64 - 127

    >>> row("FBFBBFF")
    44

    :param s: ^[FB]{7}$
    :return: row number 0 - 127
        eg: FBFBBFF -> 44
    """
    return int(s.replace('F', '0').replace('B', '1'), 2)


def col(s: str):
    """
    Decode col from 3 character string by partitioning range from 0 to 7:
        L: left - split keep lower half, eg. 0 - 3
        R: right - split, keep upper half, eg. 4 - 7

    >>> col("RLR")
    5

    :param s: ^[LR]{3}$
    :return: col number 0 - 7
        eg: RLR -> 5
    """
    return int(s.replace('L', '0').replace('R', '1'), 2)


def seat_id(row: int, col: int):
    """
    Make unique seat id from row, col

    >>> seat_id(44, 5)
    357

    :param row: 0-127
    :param col: 0-7
    :return: seat id
    """
    return row * 8 + col


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        seat_ids = [
            seat_id(*decode(line.strip()))
            for line
            in puzzle
        ]

    print('max seat_id: ', max(seat_ids))

    "all but one seat are full"
    "some seats in the front and in the back do not exist"
    all_seat_ids = set(range(min(seat_ids), max(seat_ids) + 1))
    unassigned = set(all_seat_ids).difference(seat_ids)
    print('unassigned seat: ', unassigned.pop())


