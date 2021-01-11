import numpy as np


def test(_num, _st):
    e = 0
    for _ in range(_num):
        ar = np.random.randint(1, 366, _st)    # array of random dates
        if len(np.unique(ar)) != len(ar):
            e += 1                    # count of repeat dates
    return e


st = 25     # max number of people
n = 25000   # number of sets

print("chance of having birthday at the same day")
for i in range(2, st+1):
    print("{0} people: chance == {1}%".format(i, 100*test(n, i)/n))
