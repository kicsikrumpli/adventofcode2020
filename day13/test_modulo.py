from math import gcd

from hypothesis import given, assume
from hypothesis.strategies import integers

from day13.modulo import multiplicative_inverse


@given(n=integers(min_value=1, max_value=100), m=integers(min_value=2, max_value=100))
def test_modulo_inverse(n, m):
    n_inv = multiplicative_inverse(n, m)
    if gcd(n, m) == 1:
        assert (n * n_inv) % m == 1
    else:
        assert n_inv is None


if __name__ == '__main__':
    test_modulo_inverse()