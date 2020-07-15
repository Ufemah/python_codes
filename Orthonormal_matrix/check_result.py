from Orthonormal_matrix.main import *
import unittest
# numpy was imported at main file


class Check(Matrix):
    def __init__(self, _matrix):
        super().__init__(_matrix)
        self.orthonormal_flag_check = self.is_orthonormal_check()

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


class TestFunction(unittest.TestCase):
    def test_1_equal(self):
        """
        check if wrong array return False
        """
        matr = [[0, 0, 1, 1],
                [1, 0, 0],
                [0, 1]]

        m = Matrix(matr)

        value = m.exist_flag
        expected_value = False

        self.assertEqual(value, expected_value, 'not equal')

    def test_2_equal(self):
        """
        check if matrix exist
        """
        matr = np.eye(3)

        m = Matrix(matr)

        value = m.exist_flag
        expected_value = True

        self.assertEqual(value, expected_value, 'not equal')

    def test_3_equal(self):
        """
        check if matrix is square
        """
        matr = [[0, 0, 1],
                [1, 0, 0],
                [0, 1, 0]]

        m = Matrix(matr)
        value = m.square_flag
        expected_value = True
        self.assertEqual(value, expected_value, 'not equal')

    def test_4_equal(self):
        """
        check if matrix is not square
        """
        matr = [[0, 0, 1],
                [1, 0, 0]]

        m = Matrix(matr)
        value = m.square_flag
        expected_value = False
        self.assertEqual(value, expected_value, 'not equal')

    def test_5_equal(self):
        """
        compare answers, get in different ways
        """
        matr = [[np.sqrt(2)/2, np.sqrt(2)/2],
                [-np.sqrt(2)/2, np.sqrt(2)/2]]

        m = Check(matr)
        value = m.orthonormal_flag
        expected_value = m.orthonormal_flag_check

        self.assertEqual(value, expected_value, 'not equal')


if __name__ == '__main__':
    unittest.main(verbosity=2)

