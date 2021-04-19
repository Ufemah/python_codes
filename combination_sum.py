"""
Given a set of candidate numbers (candidates) (without duplicates) and a target number (target), find
all unique combinations in candidates where the candidate numbers sums to target.

The same repeated number may be chosen from candidates unlimited number of times.

Note:

All numbers (including target) will be positive integers.
The solution set must not contain duplicate combinations.
Example 1:

Input: candidates = [2,3,6,7], target = 7,
A solution set is:
[
  [7],
  [2,2,3]
]
Example 2:

Input: candidates = [2,3,5], target = 8,
A solution set is:
[
  [2,2,2,2],
  [2,3,3],
  [3,5]
]

Constraints:

1 <= candidates.length <= 30
1 <= candidates[i] <= 200
Each element of candidate is unique.
1 <= target <= 500
"""

from typing import List


class Solution:
    def __init__(self, candidates: List[int], target: int):
        self.candidates = sorted(candidates)
        self.target = target
        self.res = set()

        self.check_input()

    def check_input(self):
        assert 1 <= len(self.candidates) <= 30, "1 <= candidates.length <= 30"

        for i in range(len(self.candidates)):
            assert 1 <= self.candidates[i] <= 200, "1 <= candidates[i] <= 200"

        assert len(self.candidates) == len(set(self.candidates)), "Each element of candidate should be unique"

        assert 1 <= self.target <= 500, "1 <= target <= 500"

    def gen(self, target, temp):
        for i in self.candidates:  # check every element on every step
            if target > i:
                self.gen(target - i, temp + [i])    # if sum of elements < target -> go to next recursive step
            elif target == i:
                temp += [i]
                temp.sort()
                self.res.add(tuple(temp))    # if sum of elements == target -> add variant to res set
                return
            else:    # if sum of elements > target -> break
                return

    def combination_sum(self) -> List[List[int]]:
        self.gen(self.target, [])   # call recursive method
        return [list(i) for i in self.res]


if __name__ == "__main__":
    s = Solution(candidates=[2, 3, 4, 6, 7], target=7)
    print(s.combination_sum())
