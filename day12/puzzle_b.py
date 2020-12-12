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


def turn(_x: int,
         _y: int,
         _turn: str,
         _turn_deg: int) -> Optional[Tuple[int, int]]:
    """
    Rotate the vector (_x, _y) left or right in 90 degree increments.

    >>> turn(2, 1, 'L', 90)
    (-1, 2)

    >>> turn(2, 1, 'R', 90)
    (1, -2)

    >>> turn(2, 1, 'R', 180)
    (-2, -1)

    :param _x: vector x to turn
    :param _y: vector y to turn
    :param _turn: 'L' for left, 'R' for right
    :param _turn_deg: degrees to turn in 90 degree increments
    :return: rotated vector
    """
    turns = {'R': (1, -1), 'L': (-1, 1)}
    if _turn in turns:
        for i in range(_turn_deg // 90):
            a, b = turns.get(_turn)
            _x, _y = _y * a, _x * b
        return _x, _y
    else:
        return None
    pass


def step() -> Generator[Tuple[int, int], Optional[Tuple[str, int]], None]:
    """
    Create generator that yields updated coordinates for received actions.

    >>> step().send(('N', 1))
    move waypoint with 1 to N to (10, 2)
    (0, 0)

    >>> gen = step()
    >>> gen.send(('R', 90))
    turning waypoint at (10, 1) R 90 degrees to (1, -10)
    (0, 0)
    >>> gen.send(('F', 3))
    go to waypoint (1, -10) 3 times
    (3, -30)

    To update coordinates, send (action, value) tuple.
        action: single character
            - one of NESW to move waypoint in a cardinal direction
            - one of LR to turn the waypoint
            - F to go forward to waypoint (waypoint moves with ship)
        value:
            - number of spaces to move waypoint
            - number of times to move forward to waypoint
            - degrees to turn in 90 degree increments

    Send None for generator to finish.
        on None, generator yields final position

    :return: generator
    """

    def _step(x: int = 0,
              y: int = 0,
              waypoint_x: int = 10,
              waypoint_y: int = 1) -> Generator[Tuple[int, int], Optional[Tuple[str, int]], None]:

        action = None
        value = None
        while True:
            if action and value:
                if action in 'NESW':
                    print('move waypoint with', value, 'to', action, end=' ')
                    dx, dy = go_cardinal(action, value)
                    waypoint_x += dx
                    waypoint_y += dy
                    print('to', (waypoint_x, waypoint_y))
                elif action in 'F':
                    print('go to waypoint', (waypoint_x, waypoint_y), value, 'times')
                    x += value * waypoint_x
                    y += value * waypoint_y
                elif action in 'LR':
                    print('turning waypoint at', (waypoint_x, waypoint_y), action, value, 'degrees to', end=' ')
                    waypoint_x, waypoint_y = turn(waypoint_x, waypoint_y, action, value)
                    print((waypoint_x, waypoint_y))

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
