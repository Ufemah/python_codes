from Matrix_analysis.main import *
import unittest
# numpy was imported at main file


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

        m = Matrix(matr)
        value = m.orthonormal_flag
        expected_value = m.orthonormal_flag_check

        self.assertEqual(value, expected_value, 'not equal')

    def test_6_equal(self):
        """
        check correct matrix
        """
        matr = np.eye(4)

        m = Matrix(matr)
        value = m.orthonormal_flag
        expected_value = True

        self.assertEqual(value, expected_value, 'not equal')

    def test_7_equal(self):
        """
        check incorrect matrix
        """
        matr = np.eye(4) + 2

        m = Matrix(matr)
        value = m.orthonormal_flag
        expected_value = False

        self.assertEqual(value, expected_value, 'not equal')

    def test_8_equal(self):
        """
        check if matrix is magic
        """
        matr = np.eye(5)

        m = Matrix(matr)
        value = m.magic_flag
        expected_value = True
        self.assertEqual(value, expected_value, 'not equal')

    def test_9_equal(self):
        """
         check if matrix is not magic
         """
        matr = [[1, 1],
                [0, 0]]

        m = Matrix(matr)
        value = m.magic_flag
        expected_value = False
        self.assertEqual(value, expected_value, 'not equal')


if __name__ == '__main__':
    unittest.main(verbosity=2)

