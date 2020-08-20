"""
A palindrome is a sequence of characters that reads the same backwards and forwards.
Given a string, s, find the longest palindromic substring in s.
"""


class Solution:
    def __init__(self, string):
        self.string = string
        print('string = {}'.format(self.string))

    def longest_palindrome_substring(self):
        pass

    def brut(self):
        length = 0
        substr = ''

        for i in range(len(self.string)):
            for j in range(len(self.string)):
                if i < j:
                    el = self.string[i:j]

                    if el == el[::-1] and len(el) > length:
                        length = len(el)
                        substr = el

                        if length > int(len(self.string) / 2) + 1:
                            return substr
        return substr


if __name__ == "__main__":
    st = "tracecars"
    s = Solution(st)
    print(s.longest_palindrome_substring())
    print(s.brut())
