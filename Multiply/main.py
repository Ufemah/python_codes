"""
Given two strings which represent non-negative integers,
multiply the two numbers and return the product as a string as well.
"""


def str_to_int(line: str) -> int:
    res = 0
    ord_zero = ord('0')
    ord_nine = ord('9')
    n = len(line)
    for i in range(n):
        if ord(line[i]) < ord_zero or ord(line[i]) > ord_nine:
            print('this string can\'t be converted to integer')
            return 0
        res += (ord(line[i]) - ord_zero) * 10**(n - i - 1)
    return res


def int_to_str(num: int) -> str:
    res = ""
    ord_zero = ord('0')
    if num == 0:
        return "0"
    while num > 0:
        res = chr((num % 10) + ord_zero) + res
        num //= 10
    return res


def multiply(str1: str, str2: str) -> str:
    n1 = str_to_int(str1)
    n2 = str_to_int(str2)
    return int_to_str(n1 * n2)


print(multiply("11", "13"))  # 143
