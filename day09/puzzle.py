from typing import List


def batch_generator(numbers: List[int], preamble_size: int = 25):
    """
    >>> for pre, n in batch_generator([1, 2, 3, 4, 5, 6], 3):
    ...     print(pre, n)
    [1, 2, 3] 4
    [2, 3, 4] 5
    [3, 4, 5] 6

    :param numbers:
    :param preamble_size:
    :return:
    """
    for i in range(len(numbers) - preamble_size):
        yield numbers[i:i + preamble_size], numbers[i + preamble_size]


def has_sum_of_n_elements(numbers: List[int],
                          target: int,
                          max_num: int = 2) -> bool:
    """
    Decide if any, exactly 'max_num' number of elements in the list 'numbers' sums to the value 'target'

    >>> has_sum_of_n_elements([1,2,3,4,5], 7)
    True

    >>> has_sum_of_n_elements([1,2,3,4,5], 3)
    True

    >>> has_sum_of_n_elements([2,3,4,5], 3)
    False

    :param numbers: to take elemnts from
    :param target: is the target sum
    :param max_num: number of elements to sum
    :return: True if 'numbers' has 'target' sum,
        otherwise False
    """
    if target == 0 and max_num == 0:
        return True
    if not numbers or max_num == 0:
        return False

    if len(numbers) > 1:
        tail = numbers[1:]
    else:
        tail = []

    head = numbers[0]

    return has_sum_of_n_elements(tail, target - head, max_num - 1) or \
           has_sum_of_n_elements(tail, target, max_num)


def contiguous_range_with_sum(
        numbers: List[int],
        target: int,
        min_length: int = 2):
    """
    Find contiguous range in 'numbers'
        that sum to 'target',
        which is at least of length 'min_length'.

    >>> contiguous_range_with_sum(numbers=[1, 2, 3, 4, 5, 6], target=9, min_length=3)
    [2, 3, 4]

    >>> contiguous_range_with_sum(numbers=[1, 2, 3, 4, 5, 6], target=50, min_length=3)
    []
    """
    for slice_len in range(min_length, len(numbers)):
        _slice = numbers[:slice_len]
        sum_slice = sum(_slice)
        if sum_slice == target:
            return _slice
        elif sum_slice > target:
            return contiguous_range_with_sum(numbers[1:], target, min_length)

    return []


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        numbers = [
            int(line)
            for line in puzzle
        ]

    has_no_sum = next((
        num
        for preamble, num in batch_generator(numbers)
        if not has_sum_of_n_elements(preamble, num)
    ))

    print('First number that has no sum in its preamble:', has_no_sum)

    contiguous_range = contiguous_range_with_sum(numbers=numbers, target=has_no_sum)
    min_max_sum = min(contiguous_range) + max(contiguous_range)
    print(f'_min_ + _max_ of contiguous range that sums to {has_no_sum}: {min_max_sum}')
