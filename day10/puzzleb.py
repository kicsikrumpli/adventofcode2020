from datetime import datetime
from typing import List, Tuple, Optional


# brute force, takes too long for puzzle
def different_chains(chargers: List[int]):
    """
    Find the number of different chains of chargers
    starting from 0
    terminating in max(chargers) + 3

    Chargers with jolatge rating difference of 1 – 3 can be chained in increasing order.

    >>> different_chains([1])
    1

    >>> different_chains([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4])
    8

    >>> different_chains([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24,
    ...                   23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35,
    ...                   8, 17, 7, 9, 4, 2, 34, 10, 3])
    19208

    :param chargers: list of chargers by joltage
    :return: number of different possible paths
    """
    def _chains(joltages: List[int], path: List[int] = None):
        if not path:
            path = []

        start = joltages[0]
        neighbors = [idx for idx, num in enumerate(joltages) if 1 <= num - start <= 3]
        # print(joltages, '|', start, ' - ', neighbors)

        _path = [*path, start]

        if start == joltages[-1]:
            # print('FOUND', _path)
            return 1

        return sum([
            _chains(joltages[neighbor:], _path)
            for neighbor in neighbors
        ])

    return _chains([0, *sorted(chargers), max(chargers) + 3])


# let's try it backwards!
def chains_backwards(chargers: List[int]):
    """
    Find the number of different chains of chargers
    starting from 0
    terminating in max(chargers) + 3

    Chargers with jolatge rating difference of 1 – 3 can be chained in increasing order.

    >>> chains_backwards([1])
    1

    >>> chains_backwards([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4])
    8

    >>> chains_backwards([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24,
    ...                   23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35,
    ...                   8, 17, 7, 9, 4, 2, 34, 10, 3])
    19208

    :param chargers: list of chargers by joltage
    :return: number of different possible paths
    """
    def _chains(joltages: List[int],
                paths_to_end: List[Optional[int]]):
        """
        Going backwards from end to start.

        memoizing all possible paths to last node from current node.
        current node is first node from the back where 'paths_to_end' is None.

        value of current node in 'paths_to_end' is sum of values where we can jump from current node.

           +-----------------+
           |                 |
           |                 v
           |     +-----------+
           |     |           |
           |     |           v
           |     |     +-----+
           |     |     |     |
           +     +     +     v
         ( 6)+>( 3)  ( 2)  ( 1)  ( 1)
           +     +   ^ +     +     ^
           |     |   | |     |     |
           |     +---+ |     +-----+
           |    1+2    |           ^
           |           |           |
           |           +-----------+
           |          1+1
           |           ^
           |           |
           +-----------+
          1+2+3

        :param joltages:
        :param paths_to_end:
        :return:
        """

        paths_none_indices = [idx for idx, p in enumerate(paths_to_end) if p is None]

        if not paths_none_indices:
            # print('done')
            return paths_to_end[0]

        current = max(paths_none_indices)
        current_value = joltages[current]
        # print(list(zip(joltages, paths_to_end)))
        # print('current node:', current, 'value:', current_value)
        neighbors = [idx for idx, n in enumerate(joltages) if 1 <= n - current_value <= 3]
        # print('neighbors of current node:', neighbors, 'values', [joltages[neighbor] for neighbor in neighbors])
        paths_to_end[current] = sum([paths_to_end[neighbor] for neighbor in neighbors])
        return _chains(joltages, paths_to_end)

    chargers = [0, *sorted(chargers), max(chargers) + 3]
    paths_to_end: List[Optional[int]] = [None for _ in range(len(chargers))]
    paths_to_end[-1] = 1
    return _chains(chargers, paths_to_end)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        chargers = [int(line) for line in puzzle]

    a = chains_backwards(chargers)
    print(a)
