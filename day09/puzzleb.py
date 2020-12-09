from typing import List


def range_with_sum(all_numbers: List[int],
                   target: int,
                   sum: int = 0,
                   numbers_slice: List[int] = None,
                   ):
    """
    >>> range_with_sum([1,2,3,4,5,6], 10)
    [1, 2, 3, 4]

    >>> range_with_sum([1,2,3,4,5,6], 9)
    [2, 3, 4]

    >>> range_with_sum([1,2,3,4,5,6], 50)
    []

    """
    # print(numbers_slice, all_numbers)
    if not numbers_slice:
        numbers_slice = []

    if sum == target:
        # print('found')
        return numbers_slice
    elif not all_numbers and sum < target:
        # print('all num empty')
        return []
    elif sum < target:
        # print('sum < target: ', sum, '<', target)
        return range_with_sum(all_numbers=all_numbers[1:],
                              target=target,
                              sum=sum + all_numbers[0],
                              numbers_slice=[*numbers_slice, all_numbers[0]])
    else:  # sum > target:
        # print('---')
        return range_with_sum(all_numbers=[*numbers_slice, *all_numbers][1:],
                              target=target)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(range_with_sum([1, 2, 3, 4, 5, 6], 30))
