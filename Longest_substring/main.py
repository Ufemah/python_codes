"""
Given a string, find the length of the longest substring without repeating characters
"""


class Solution:
    def __init__(self, string):
        self.string = string
        print(self.string)

    def length_of_substring(self):
        pass

    def long_way(self):
        """
        easy and slow
        :return: length of longest substr w/o repeating
        """
        res = 0

        for i in range(len(self.string)):
            for j in range(len(self.string)):
                if i < j:
                    if len(self.string[i:j]) == len(set(self.string[i:j])) and len(self.string[i:j]) > res:
                        res = len(self.string[i:j])

        return res


if __name__ == '__main__':
    inp = 'abrka' + 'abcdefghij' + 'jxxx'
    s = Solution(inp)
    print(s.length_of_substring())   # 10
    print(s.long_way())
