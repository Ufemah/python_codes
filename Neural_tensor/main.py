import tensorflow as tf
from benchmark import benchmark

print(tf.config.list_physical_devices('GPU'))


@benchmark
def func():
    c1 = tf.random.normal([10000, 10000], 0, 10, tf.float32)
    c2 = tf.random.normal([10000, 10000], 0, 10, tf.float32)
    return tf.matmul(c1, c2)


print(func())

