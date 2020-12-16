from typing import List, Iterator


def step(numbers: List[int]) -> Iterator[int]:
    """
    In this game, the players take turns saying numbers.
    They begin by taking turns reading from a list of _starting numbers_.
    Then, each turn consists of considering the most recently spoken number:
    - If that was the first time the number has been spoken, the current player says 0.
    - Otherwise, the number had been spoken before;
        the current player announces how many turns apart the number is
        from when it was previously spoken.

    >>> stepper = step([0, 3, 6])
    >>> [next(stepper) for _ in range(7)]
    [0, 3, 3, 1, 0, 4, 0]

    >>> for starting_nums in [[1, 3, 2], [2, 1, 3], [1, 2, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2]]:
    ...     stepper = step(starting_nums)
    ...     for _ in range(3, 2020):
    ...         a = next(stepper)
    ...     print(a)
    1
    10
    27
    78
    438
    1836

    :param numbers: starting numbers
    """
    history = {num: idx for idx, num in enumerate(numbers[:-1])}
    round = len(numbers) - 1
    last_num = numbers[-1]

    while True:
        if round % 100000 == 0:
            print('round:', round)
        if last_num not in history:
            _last_num = last_num
            last_num = 0
            history[_last_num] = round
        else:
            _last_num = last_num
            last_num = round - history[last_num]
            history[_last_num] = round

        round += 1
        yield last_num


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        starting_numbers = [int(num) for num in puzzle.readline().split(',')]

    stepper = step(starting_numbers)
    rounds = 30000000
    for _ in range(len(starting_numbers), rounds):
        num = next(stepper)

    print(f'last number spoken after {rounds} rounds: {num}')
