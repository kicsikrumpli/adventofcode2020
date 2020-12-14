from math import gcd
from typing import Optional


def multiplicative_inverse(n: int, m: int) -> Optional[int]:
    """
    n^-1 * n === 1 (mod m)

    >>> multiplicative_inverse(17, 29)
    12

    :param n: number to find the multiplicative inverse of
    :param m: modulus
    :return: inverse of n
    """
    if gcd(n, m) != 1:
        return None
    else:
        for n_1 in range(m):
            if (n_1*n) % m == 1:
                return n_1


if __name__ == '__main__':
    import doctest
    doctest.testmod()
