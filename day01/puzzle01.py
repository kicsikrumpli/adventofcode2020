from functools import reduce
from typing import List, Optional


def find_summands(goal: int,
                  nums: List[int],
                  max_depth,
                  resp: Optional[List[int]] = None,
                  ):
    if resp is None:
        resp = []

    if goal == 0 and max_depth == 0:
        return resp
    if not nums:
        return None
    if max_depth == 0:
        return None

    return \
        find_summands(goal, nums[1:], max_depth, resp) or \
        find_summands(goal-nums[0], nums[1:], max_depth-1, [*resp, nums[0]])


if __name__ == '__main__':
    numbers = []
    with open('input.txt', 'rt') as puzzle_input:
        for line in puzzle_input:
            numbers.append(int(line))

    n = find_summands(2020, numbers, 3)
    print(f'sum({n}) = {sum(n)}')
    print(reduce(lambda a, b: a*b, n))
