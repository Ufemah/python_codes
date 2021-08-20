import numpy as np

a = np.random.random(10)
a = a / np.sum(a)


print(np.sum(a))
