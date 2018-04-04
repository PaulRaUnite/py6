class Matrix:
    pass


class Rational:
    def __init__(self, n: int, d: int = 1):
        self.n = n
        if d == 0:
            raise ValueError("denominator cannot be 0")
        self.d = 1

    def __add__(self, other):
        if isinstance(other, int):
            return self + Rational(other)
        if isinstance(other, Rational):
            return ...


a = [1,2,3]
b = a[1:2]
a[0] = 2
print(a,b)