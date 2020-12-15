from typing import List


def step(numbers: List[int], next_number: int = None) -> List[int]:
    """

    >>> steps = step([], 0)
    >>> steps = step(steps, 3)
    >>> steps = step(steps, 6)
    >>> for _ in range(7):
    ...     steps = step(steps)
    >>> steps
    [0, 4, 0, 1, 3, 3, 0, 6, 3, 0]

    >>> for steps in [[1, 3, 2], [2, 1, 3], [1, 2, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2]]:
    ...      steps.reverse()
    ...      for _ in range(len(steps), 2020):
    ...          steps = step(steps)
    ...      steps[0]
    1
    10
    27
    78
    438
    1836

    :param numbers: numbers seen so far in reverse order
        first element is number seen last
        last element is number seen first
    :param next_number: add starting number
    :return: number history
    """
    if next_number is not None:
        return [next_number, *numbers]

    last_spoken, *rest = numbers
    if last_spoken not in rest:
        return [0, *numbers]

    latest_index = rest.index(last_spoken) + 1
    return [latest_index, *numbers]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        starting_numbers = [int(num) for num in puzzle.readline().split(',')]

    starting_numbers.reverse()
    history = starting_numbers
    rounds = 2020
    # rounds = 30000000
    for r in range(len(starting_numbers), rounds):
        history = step(history)

    print(f'last number spoken after {rounds} rounds: {history[0]}')
