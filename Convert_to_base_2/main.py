from math import log2


def base_2(n):
    res = ''
    i = int(log2(n))

    while i >= 0:
        if (n - 2**i) >= 0:
            res += '1'
            n -= 2**i
        else:
            res += '0'
        i -= 1

    return res


if __name__ == '__main__':
    print(base_2(123))
