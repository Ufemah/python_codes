import numpy as np


class Matrix:
    def __init__(self, _matrix):
        self.matrix = np.array(_matrix)
        self.exist_flag = self.is_matrix()
        self.square_flag = self.is_square()
        self.orthonormal_flag = self.is_orthonormal()

    def is_matrix(self):
        temp = len(self.matrix[0])
        for i in self.matrix:
            if len(i) != temp:
                return False
        return True

    def is_square(self):
        if not self.exist_flag:
            return False
        if len(self.matrix) != len(self.matrix.T):
            return False
        return True

    def is_orthonormal(self):
        if not self.square_flag or not self.exist_flag:
            return False
        if np.all(np.eye(len(self.matrix)) == self.matrix.dot(self.matrix.T)):
            return True
        return False

    def show(self):
        print("Your input: \n{}".format(self.matrix))
        print("Is matrix: {}".format(self.exist_flag))
        print("Square: {}".format(self.square_flag))
        print("Orthonormal: {}".format(self.orthonormal_flag))


if __name__ == "__main__":
    matrix = [[0, 0, 1],
              [1, 0, 0],
              [0, 1, 0]]

    m = Matrix(matrix)
    m.show()
