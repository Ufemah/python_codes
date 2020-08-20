"""
Given a string, find the length of the longest substring without repeating characters
"""


class Solution:
    def __init__(self, string):
        self.string = string
        print(self.string)

    def length_of_substring(self):
        """
        good solution
        :return: length of longest substr w/o repeating
        """
        length = 0
        res = ''
        substr = ''

        for el in self.string:

            if el in res:
                if len(res) > length:
                    length = len(res)
                    substr = res
                res = res[res.index(el) - 1::][1::]
            else:
                res += el

            if length > int(len(self.string) / 2) + 1:
                return length

        # print(substr)
        return length

    def long_way(self):
        """
        easy and slow
        :return: length of longest substr w/o repeating
        """
        length = 0
        substr = ''

        for i in range(len(self.string)):
            for j in range(len(self.string)):
                if i < j:
                    el = self.string[i:j]

                    if len(el) == len(set(el)) and len(el) > length:
                        length = len(el)
                        substr = el

                        if length > int(len(self.string) / 2) + 1:
                            return length
        # print(substr)
        return length


if __name__ == '__main__':
    inp = 'abrka' + 'abcdefghij' + 'jxxx'
    s = Solution(inp)
    print(s.length_of_substring())   # 10
    print(s.long_way())              # 10
