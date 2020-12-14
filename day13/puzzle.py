from typing import List, Tuple
from io import StringIO


def parse(puzzle) -> Tuple[int, List[int]]:
    """
    parse input text

    >>> parse(StringIO("123\\n1,2,x,3,x"))
    (123, [1, 2, 3])

    :param puzzle: file like object with input
    :return:
    """
    timestamp = int(puzzle.readline())
    bus_ids = [
        int(bus_id)
        for bus_id
        in puzzle.readline().split(',')
        if bus_id.isnumeric()
    ]
    return timestamp, bus_ids


def next_departure(timestamp: int, bus_ids: List[int]) -> Tuple[int, int]:
    """
    What is the ID of the earliest bus you can take to the airport
    multiplied by the number of minutes you'll need to wait for that bus?
         n*d        (n+1)*d
    ------|-----------|---------
               ^------+----^
               x      |   x+d
          | a  |   ?  |
    x: timestamp
    d: departure interval == bus id
    a: time since last departure: x % d
    ?: time to next departure: d - (x % d)
    """
    print('timestamp:', timestamp)
    print('bus id-s:', bus_ids)
    time_to_departures = [bus_id - (timestamp % bus_id) for bus_id in bus_ids]
    print('time to next departure:', time_to_departures)

    all_zero = [(timestamp + departure) % bus_id for bus_id, departure in zip(bus_ids, time_to_departures)]
    assert all(z == 0 for z in all_zero)

    bus_id, till_next_departure = min(zip(bus_ids, time_to_departures), key=lambda x: x[1])
    print('time to next departure', till_next_departure)
    print('bus', bus_id)
    return till_next_departure, bus_id


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        timestamp, bus_ids = parse(puzzle)

    time, bus_id = next_departure(timestamp, bus_ids)
    print('-'*10)
    print('departure time * bus id:', time * bus_id)
