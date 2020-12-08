from collections import defaultdict
from typing import Tuple, List, Dict, Set


def parse_sentence(sentence: str) -> Tuple[str, List[Tuple[str, int]]]:
    """
    Find what kinds, and how many of bags the outer bag contains, as described in a sentence.

    NB! there is no fun in regex....

    >>> parse_sentence("light red bags contain 1 bright white bag, 2 muted yellow bags.")
    ('light red', [('bright white', 1), ('muted yellow', 2)])

    >>> parse_sentence("dark orange bags contain 3 bright white bags, 4 muted yellow bags.")
    ('dark orange', [('bright white', 3), ('muted yellow', 4)])

    >>> parse_sentence("bright white bags contain 1 shiny gold bag.")
    ('bright white', [('shiny gold', 1)])

    >>> parse_sentence("faded blue bags contain no other bags.")
    ('faded blue', [])

    :param sentence: describes bags
    :return: tuple of outer bag, possible contained bag type and number
    """
    outer_bag, contents = sentence.split(" bags contain ")
    inner_bags = contents\
        .strip()\
        .strip('.')\
        .replace(' bags', '')\
        .replace(' bag', '')\
        .split(', ')
    bags = [
        (" ".join(bag.split()[1:]), int(bag.split()[0]))
        for bag in inner_bags
        if bag != 'no other'
    ]
    return outer_bag, bags


def discard_num(parsed_bag: Tuple[str, List[Tuple[str, int]]]) -> Tuple[str, List[str]]:
    """
    Discard number of bags from content.

    >>> discard_num(('dark orange', [('bright white', 3), ('muted yellow', 4)]))
    ('dark orange', ['bright white', 'muted yellow'])

    :param parsed_bag: output of parse_sentence
    :return: tuple of bag, list of contents
    """
    bag, contents = parsed_bag
    return bag, [inner_bag for inner_bag, num in contents]


def make_index(file) -> Dict[str, List[str]]:
    """
    Make index from sentences.
    Key is the container bag,
    values are the bags that can be placed inside it

    >>> make_index([
    ...     "light red bags contain 1 bright white bag, 2 muted yellow bags.",
    ...     "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
    ...     ])
    {'light red': ['bright white', 'muted yellow'], 'dark orange': ['bright white', 'muted yellow']}

    :param file: of all the sentences
    :return: index
    """
    return dict(
        discard_num(parse_sentence(sentence))
        for sentence in file
    )


def make_index_with_nums(file) -> Dict[str, List[Tuple[str, int]]]:
    return dict(
        parse_sentence(sentence)
        for sentence in file
    )


def invert_index(index: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Makes dict from index, where
    key is a contained bag,
    values are the bags that can hold contained bag
    >>> invert_index({'a': ['b', 'c']})
    {'b': ['a'], 'c': ['a']}
    """
    inverted_index = defaultdict(lambda: list())
    for key, values in index.items():
        for value in values:
            inverted_index[value].append(key)
    return dict(inverted_index)


def traverse_outwards(bags, start, visited=None):
    """
    Follow all possible paths from inside outwards.

    To answer the question: How many bag colors can eventually contain at least one shiny gold bag?
    We need to count all the distinct bag colors we encounter on the paths.

    :param bags: _inverted index_ of bags:
        key: contained bag
        values: bags that can contain key
    :param start: node to start traversing from
    :param visited: keeps track of visited nodes
    :return: all visited nodes
    """
    if visited is None:
        visited = set()

    for bag in bags.get(start, []):
        if bag not in visited:
            visited.add(bag)
            traverse_outwards(bags=bags, start=bag, visited=visited)

    return visited


def count_inwards(bags: Dict[str, List[Tuple[str, int]]], start: str):
    """
    How many bags are inside a bag.

    >>> count_inwards({
    ...         'a': [('b', 1), ('c', 2)]
    ...     }, 'a')
    3

    >>> count_inwards({
    ...         'shiny gold': [('dark red', 2)],
    ...         'dark red': [('dark orange', 2)],
    ...         'dark orange': [('dark yellow', 2)],
    ...         'dark yellow': [('dark green', 2)],
    ...         'dark green': [('dark blue', 2)],
    ...         'dark blue': [('dark violet', 2)],
    ...     }, 'shiny gold')
    126

    Answers the question: "How many individual bags are required inside your single shiny gold bag?"
    :param bags: dict of bags, where
        key: containing bag
        value: list of (bag, number)-s contained in key
    :param start: forst node of traversal
    :return: number of bags inside
    """
    count = 0
    for bag, n in (contents for contents in bags.get(start, [])):
        count += n + n * count_inwards(bags=bags, start=bag)

    return count


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        inverted_index = invert_index(make_index(puzzle))

    v = traverse_outwards(bags=inverted_index, start='shiny gold')
    print('number of kinds of bags that can eventually contain a _shiny gold_ bag:', len(v))

    with open('input.txt', 'rt') as puzzle:
        index = make_index_with_nums(puzzle)

    bags_inside = count_inwards(bags=index, start='shiny gold')
    print('number of bags inside a _shiny gold_ bag: ', bags_inside)
