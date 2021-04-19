"""
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
An input string is valid if:
- Open brackets are closed by the same type of brackets.
- Open brackets are closed in the correct order.
- Note that an empty string is also considered valid.
"""


class Solution:
    def __init__(self, string):
        self.string = string
        print(self.string)

    def is_validate(self):
        brackets = {')': '(', ']': '[', '}': '{'}
        seen = []

        if self.string == "":
            return True

        if len(self.string) % 2 != 0:
            return False

        for el in self.string:
            if el in brackets.values():
                seen.append(el)

            if len(seen) != 0:
                if el in brackets.keys() and seen[-1] == brackets[el]:
                    seen.pop()

            else:
                return False   # if some element is not bracket

        if len(seen) != 0:
            return False    # if order is not correct

        return True


if __name__ == '__main__':
    s = "()(){(())"
    print(Solution(s).is_validate())
