from typing import List


def is_valid(_min: str, _max: str, ch: str, passwd: str) -> bool:
    parts = passwd.split(ch)
    return int(_min) < len(parts) <= int(_max) + 1


def is_valid2(pos_a: str, pos_b: str, ch: str, passwd: str) -> bool:
    a = passwd[int(pos_a) - 1] == ch
    b = passwd[int(pos_b) - 1] == ch
    return a ^ b


def split_tokens(line: str) -> List[str]:
    return line\
        .replace('-', '|')\
        .replace(' ', '|')\
        .replace(':', '')\
        .split('|')


if __name__ == '__main__':
    with open('input.txt', 'rt') as puzzle:
        valid = [1
                 for line
                 in puzzle
                 # if is_valid(*split_tokens(line))]
                 if is_valid2(*split_tokens(line))]
    print(sum(valid))
