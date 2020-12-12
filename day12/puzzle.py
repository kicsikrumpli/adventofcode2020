from typing import Generator, Tuple, Optional


def go_cardinal(_dir: str, _step: int) -> Optional[Tuple[int, int]]:
    """
    Step in a cardinal direction.

    >>> go_cardinal('N', 3)
    (0, 3)

    >>> go_cardinal('E', 3)
    (3, 0)

    >>> go_cardinal('S', 3)
    (0, -3)

    >>> go_cardinal('W', 3)
    (-3, 0)

    >>> go_cardinal('x', 1)

    :param _dir: cardinal direction, one of N,E,S,W
    :param _step: number of steps
    :return: tuple of (N, E) steps
    """
    dirs = {
        'N': (0, 1),
        'E': (1, 0),
        'S': (0, -1),
        'W': (-1, 0)
    }
    if _dir in dirs:
        dx, dy = dirs.get(_dir)
        return _step * dx, _step * dy
    else:
        return None


def turn(_heading: str,
         _turn: str,
         _turn_deg: int) -> Optional[str]:
    """
    Turn left / right from heading.

    >>> turn('N', 'L', 90)
    'W'

    >>> turn('N', 'R', 90)
    'E'

    >>> turn('S', 'R', 180)
    'N'

    >>> turn('S', 'L', 180)
    'N'

    :param _heading: original heading
        one of NESW
    :param _turn: direction of turn
        one of LR
    :param _turn_deg: degrees to turn
        multiple of 90
    :return: new heading
    """
    headings = ['N', 'E', 'S', 'W']
    turns = {'R': +1, 'L': -1}
    if _heading in headings and _turn in turns:
        index = headings.index(_heading)
        _dir = turns[_turn]
        index = (index + _dir * _turn_deg // 90) % 4
        return headings[index]
    else:
        return None
    pass


def step() -> Generator[Tuple[int, int], Optional[Tuple[str, int]], None]:
    """
    Create generator that generates updated coordinates for received actions.

    >>> step().send(('N', 1))
    going 1 in the cardinal direction N
    (0, 1)

    >>> gen = step()
    >>> gen.send(('R', 90))
    turning from heading E to heading S
    (0, 0)
    >>> gen.send(('F', 3))
    going forward 3 in heading S
    (0, -3)

    To update coordinates, send (action, value) tuple.
        action: single character
            - one of NESW to go in a cardinal direction
            - one of LR to turn
            - F to go forward in heading
        value:
            - number of spaces to move
            - degrees to turn in 90 degree increments

    Send None for generator to finish.
        on None, generator yields final position

    :param x: starting x coordinate
    :param y: starting y coordinate
    :param heading: starting heading

    :return: generator
    """

    def _step(x: int = 0,
              y: int = 0,
              heading: str = 'E') -> Generator[Tuple[int, int], Optional[Tuple[str, int]], None]:

        action = None
        value = None
        while True:
            if action and value:
                if action in 'NESW':
                    print('going', value, 'in the cardinal direction', action)
                    dx, dy = go_cardinal(action, value)
                elif action in 'F':
                    print('going forward', value, 'in heading', heading)
                    dx, dy = go_cardinal(heading, value)
                else:
                    dx, dy = 0, 0

                if action in 'LR':
                    print('turning from heading', heading, end=' ')
                    heading = turn(heading, action, value)
                    print('to heading', heading)

                x += dx
                y += dy

            command = yield x, y
            if not command:
                break
            else:
                action, value = command

        yield x, y

    gen = _step()
    next(gen)
    return gen


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    gen = step()
    with open('input.txt', 'rt') as puzzle:
        for line in puzzle:
            action = line[0]
            value = int(line[1:])
            print(gen.send((action, value)))

    x, y = gen.send(None)
    print('Manhattan distance at end of instructions: ', abs(x)+abs(y))
