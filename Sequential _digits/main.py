"""
An integer has sequential digits if and only if each digit in the number is one more than the previous digit.

Return a sorted list of all the integers in the range [low, high] inclusive that have sequential digits.

Input: low = 1000, high = 13000
Output: [1234,2345,3456,4567,5678,6789,12345]
"""

from typing import List


class Solution:
    def __init__(self, low, high):
        assert 10 <= low <= high <= 10 ** 9, "10 <= low <= high <= 10**9"
        self.low = low
        self.high = high

        self.res = []

    def generator(self, n):
        if self.low <= n <= self.high:
            self.res.append(n)

        if (n % 10) + 1 < 10:
            return self.generator(n * 10 + n % 10 + 1)

    def sequential_digits(self) -> List[int]:
        self.res = []

        for i in range(1, 9 + 1):
            self.generator(i)

        return sorted(self.res)

    def brut_gen(self):
        set = "1234567890"

        res = []
        for i in range(len(str(self.low)), len(str(self.high)) + 1):
            for j in range(len(set) - i):
                temp = int(set[j:j + i])
                if self.high >= temp >= self.low:
                    res.append(temp)

        return res


if __name__ == "__main__":
    s = Solution(100, 13000)
    print(s.sequential_digits())
    print(s.brut_gen())
