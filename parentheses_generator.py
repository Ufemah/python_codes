"""
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
"""

from typing import List


class Solution:
    def __init__(self):
        self.n = 0
        self.res = []

    def generator(self, s, to_open, to_close):
        if to_open > to_close:
            return

        elif to_open == 0 and to_close == 0:
            self.res.append(s)
            return

        elif to_open == 0:
            self.generator(s + ')', to_open, to_close - 1)

        else:
            self.generator(s + '(', to_open - 1, to_close)
            self.generator(s + ')', to_open, to_close - 1)

    def generate_parentheses(self, n: int) -> List[str]:
        self.n = n
        self.res = []   # clean res before generating
        
        self.generator(s='', to_open=self.n, to_close=self.n)
        return self.res


print(Solution().generate_parentheses(3))
