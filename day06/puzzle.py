from functools import reduce
from typing import Set, List


def group_generator(file):
    """
    Generates groups from file separated by blank lines.
    Lines of a group are returned as a list of lines.

    >>> for group in group_generator(['abc', 'def', '', 'ghi', 'jkl']):
    ...     print(group)
    ['abc', 'def']
    ['ghi', 'jkl']

    :param file: file like object to parse groups from
    :return: generator
    """
    group = []
    for line in file:
        line = line.strip()
        if not line:
            yield group
            group = []
        else:
            group.append(line)
    if group:
        yield group


def any_yes(lines: List[str]) -> Set[str]:
    """
    Find questions to which everybody responded with yes.

    groups are separated by blank lines
    each line represents one person in a group
    each character marks a question to which the person responded with a yes

    >>> sorted(any_yes(['abc', 'a']))
    ['a', 'b', 'c']

    >>> sorted(any_yes(['a', 'b']))
    ['a', 'b']

    :param lines: group response
        each line marks yes responses of a single person
    :return: set of questions to which anyone in the group reponded with yes
    """
    responses = set()
    for line in lines:
        responses = responses.union(c for c in line)
    return responses


def all_yes(lines: List[str]):
    """
    Find questions to which everybody responded with yes.

    groups are separated by blank lines
    each line represents one person in a group
    each character marks a question to which the person responded with a yes

    >>> print(sorted(all_yes(['abc'])))
    ['a', 'b', 'c']

    >>> print(sorted(all_yes(['a', 'b', 'c'])))
    []

    >>> print(sorted(all_yes(['ab', 'ac'])))
    ['a']

    >>> print(sorted(all_yes(['a', 'a', 'a', 'a'])))
    ['a']

    >>> print(sorted(all_yes(['b'])))
    ['b']

    :param lines: group response
        each line marks yes responses of a single person
    :return: set of questions to which everyone in the group reponded with yes
    """
    responses = []
    for line in lines:
        responses.append(set(c for c in line))
    return reduce(set.intersection, responses)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        any_counts = [
            len(any_yes(lines))
            for lines
            in group_generator(puzzle)
        ]
    print('total group any yes: ', sum(any_counts))

    with open('input.txt', 'rt') as puzzle:
        all_counts = [
            len(all_yes(lines))
            for lines
            in group_generator(puzzle)
        ]
    print('total group all yes: ', sum(all_counts))
