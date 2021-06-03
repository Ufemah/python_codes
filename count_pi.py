"""
Perform an approximate calculation of π.
To do this, calculate the perimeter of an equilateral polygon and use p = 2r*pi
"""

from math import sqrt, pi


class CountPi:
    def __init__(self):
        self.value = 0
        self.radius = 1
        self.side = sqrt(2) * self.radius
        self.sides_count = 4
        self.max_steps = 100000

    def main(self):
        if self.sides_count < self.max_steps:

            a = self.side / 2
            b = self.radius - sqrt(self.radius**2 - a**2)
            self.side = sqrt(a**2 + b**2)

            perimeter = self.sides_count * self.side * 2

            self.value = perimeter / (2 * self.radius)

            self.sides_count *= 2

            self.show()
            self.main()

        return self.value

    def show(self):
        print(f"n = {self.sides_count}, pi = {self.value}")


if __name__ == "__main__":
    p = CountPi()
    res = p.main()
    print(f"true pi = {pi}")
