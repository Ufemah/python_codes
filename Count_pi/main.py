"""
Perform an approximate calculation of π.
To do this, calculate the perimeter of an equilateral polygon and use p = 2r*pi
"""

import numpy as np


def count_pi():

    radius = 1    # can be any number, except 0
    iters = 1000000

    count = np.arange(3, iters + 3, 1)    # count of sides
    angles_cos = np.cos(2 * np.pi / count)    # cos of central angle for cos theorem
    perimeter = np.sqrt((2 * radius**2) * (1 - angles_cos)) * count     # side length * count
    pi = perimeter / (2 * radius)

    print("approximate pi: {}".format(pi[-1]))
    print("true pi == {0}".format(np.pi))


if __name__ == "__main__":
    count_pi()
