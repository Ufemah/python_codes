import numpy as np


class Neural:
    def __init__(self):
        self.weights = 2 * np.random.random((3, 1)) - 1  # generate random weights (-1 <= weights <= 1)

    def sigmoid(self, x):
        """
        activation function
        """
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def work(self, inputs):
        return self.sigmoid(np.dot(inputs, self.weights))

    def train(self, inp, correct_out, steps_count):
        for _ in range(steps_count):

            output = self.work(inp)

            error = correct_out - output

            if _ == 0 or _ == steps_count - 1:
                print("error\n", sum(error**2), "\n")

            adjustments = np.dot(inp.T, error * self.sigmoid_derivative(output))

            self.weights += adjustments


if __name__ == "__main__":
    n = Neural()

    print("start weights:")
    print(n.weights)

    training_input = np.array([[0, 1, 0],
                               [0, 0, 1],
                               [1, 0, 0],
                               [1, 1, 0],
                               [1, 1, 1]])

    training_output = np.array([[1, 0, 0, 1, 1]]).T

    n.train(training_input, training_output, 10000)

    print("weights after training")
    print(n.weights)

    example = np.array([0, 0, 1])
    print("test example:", example)

    print("result:", n.work(example))
