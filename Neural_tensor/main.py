import tensorflow as tf

print(tf.config.list_physical_devices('GPU'))


def func():
    c1 = tf.random.normal([1000, 1000], 0, 10, tf.float32)
    c2 = tf.random.normal([1000, 1000], 0, 10, tf.float32)
    return tf.matmul(c1, c2)


if __name__ == "__main__":
    print(func())

