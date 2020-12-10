from itertools import groupby
from typing import List


def differences(jolts: List[int], terminal_diff: int = 3):
    """
    Connect all the chargers.
    Each one in the chain must be rated 1 – 3 jolts higher than the previous.
    starting 0, and terminal 3 higher than max automatically added.

    >>> differences([1, 3, 4, 7])
    {1: 2, 2: 1, 3: 2}

    >>> differences([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4])
    {1: 7, 3: 5}

    >>> differences([28, 33, 18, 42, 31, 14, 46, 20, 48, 47,
    ...         24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35,
    ...         8, 17, 7, 9, 4, 2, 34, 10, 3])
    {1: 22, 3: 10}


    :param jolts: charger ratings
    :param terminal_diff: terminal is rated this much higher than max rating of all chargers
    :return: number of charger rating differences
        key: rating difference in charger chain
        value: number of rating difference in chain
    """
    jolts = sorted([*jolts, max(jolts) + terminal_diff])
    neighbors = [0, *jolts]
    difference_pairs = list(zip(neighbors, jolts))
    diffs = [higher - lower for lower, higher in difference_pairs]
    diff_counts = {diff: len(list(num)) for diff, num in groupby(sorted(diffs))}
    return diff_counts


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        joltages = [int(line) for line in puzzle]

    diffs = differences(joltages)
    print('Product of number of 1 and 3 joltage differences: ', diffs[1] * diffs[3])
