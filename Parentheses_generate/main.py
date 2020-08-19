"""
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
"""

from typing import List


class Solution:
    def __init__(self, num: int):
        self.n = num
        self.res = []

        print("num = {}".format(self.n))

    def generator(self, s, to_open, to_close):
        if to_open > to_close:
            return
        elif to_open == 0 and to_close == 0:
            self.res.append(s)
        elif to_open == 0:
            self.generator(s + ')', to_open, to_close - 1)
        else:
            self.generator(s + '(', to_open - 1, to_close)
            self.generator(s + ')', to_open, to_close - 1)

    def generate_parentheses(self) -> List[str]:
        self.generator(s='', to_open=self.n, to_close=self.n)
        return self.res


print(Solution(3).generate_parentheses())
