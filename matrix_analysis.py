import numpy as np


class Matrix:
    def __init__(self, _matrix):
        self.eps = 0.00000001    # accuracy
        try:
            self.matrix = np.array(_matrix)
            self.exist_flag = self.is_matrix()
            self.square_flag = self.is_square()
            self.orthonormal_flag = self.is_orthonormal()
            self.orthonormal_flag_check = self.is_orthonormal_check()
            self.magic_flag = self.is_magic()

        except TypeError:
            self.matrix = None
            self.exist_flag = False
            self.square_flag = False
            self.orthonormal_flag = False
            self.orthonormal_flag_check = False
            self.magic_flag = False

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
        diff = self.matrix.dot(self.matrix.T) - np.eye(len(self.matrix))
        if np.all(diff <= self.eps):
            return True
        return False

    def is_orthonormal_check(self):
        """
        another way to check orthonormality
        """
        if not self.exist_flag or not self.square_flag:
            return False

        for i1 in self.matrix:
            for i2 in self.matrix:
                if np.all(i1 == i2) and np.all((abs(i1.dot(i2)) - 1) > self.eps):
                    return False

                if np.all(i1 != i2) and np.all((abs(i1.dot(i2))) > self.eps):
                    return False

        return True

    def is_magic(self):
        """
        Matrix is called magic square if sum of elements of all strings and all columns is the same
        """
        if not self.square_flag or not self.exist_flag:
            return False

        ones = np.ones_like(self.matrix)[0]

        if np.any(ones.dot(self.matrix) != ones.dot(self.matrix.T)):
            return False

        return True

    def show(self):
        print("Your input: \n{}".format(self.matrix))
        print("Is matrix: {}".format(self.exist_flag))
        print("Square: {}".format(self.square_flag))
        print("Orthonormal: {}".format(self.orthonormal_flag))
        print("Magic: {}".format(self.magic_flag))


if __name__ == "__main__":
    matrix = [[0, 0, 1],
              [1, 0, 0],
              [0, 1, 0]]

    m = Matrix(matrix)
    m.show()
