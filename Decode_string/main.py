"""
Given an encoded string, return its decoded string.

The encoding rule is: k[encoded_string], where the encoded_string
inside the square brackets is being repeated exactly k times.

Note that k is guaranteed to be a positive integer.

You may assume that the input string is always valid; No extra white spaces, square brackets are well-formed, etc.

Furthermore, you may assume that the original data does not contain any digits and that digits are only for
those repeat numbers, k. For example, there won't be input like 3a or 2[4].
"""

import re

pat = r"\d+\[\w+\]"


class Solution:
    def __init__(self, s: str):
        self.line = s
        print(self.line)

    def decode_string(self) -> str:
        elements = re.findall(pat, self.line)
        for el in elements:
            temp = el
            el = el[:-1:]
            el = el.split('[')   # [k: int, encoded_string: str]
            self.line = self.line.replace(temp, int(el[0]) * el[1])
        if '[' in self.line:
            return self.decode_string()
        else:
            return self.line


if __name__ == "__main__":
    line = "3[a2[c]]"
    print(Solution(line).decode_string())    # "aaabcbc"
