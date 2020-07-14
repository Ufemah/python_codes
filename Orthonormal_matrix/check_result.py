from Orthonormal_matrix.main import *
import unittest
# numpy was imported at main file


class Check(Matrix):
    def __init__(self, _matrix):
        super().__init__(_matrix)

    def is_orthonormal_check(self):
        for i1 in self.matrix:
            for i2 in self.matrix:
                if (np.all(i1 == i2) and np.all(i1.T.dot(i2) != 1)) or (np.all(i1 != i2) and np.all(i1.T.dot(i2) != 0)):
                    return False
        return True


class TestFunction(unittest.TestCase):
    def test_1_equal(self):

        matr = [[0, 0, 1],
                [1, 0, 0],
                [0, 1, 0]]

        m = Check(matr)
        value = m.is_orthonormal()
        expected_value = m.is_orthonormal_check()

        self.assertEqual(value, expected_value, 'not equal')


if __name__ == '__main__':
    unittest.main(verbosity=2)

