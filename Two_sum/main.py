"""
You are given a list of numbers, and a target number k.
Return whether or not there are two numbers in the list that add up to k.
"""

from typing import List


def two_sum(lst: List[int], k: int) -> bool:

    if k % 2 == 1:    # lst elements can't duplicate, because (a + a == 2a) != (k == 2b + 1)
        lst = set(lst)

    seen = set()

    for el in lst:
        temp = k - el
        if temp in seen:
            return True
        seen.add(el)
    return False


if __name__ == '__main__':
    print(two_sum(lst=[4, 7, 1, -3, 2], k=5))
