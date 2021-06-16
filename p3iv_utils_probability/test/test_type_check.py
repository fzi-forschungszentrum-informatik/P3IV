import unittest
import logging
import numpy as np
from util_probability.distributions.base.normal import type_check


class TestTypeCheck(unittest.TestCase):
    def test_type_check_array_mean(self):
        input1 = np.array([1, 2])
        output1 = type_check(input1, 1, 2)
        self.assertEqual(output1.shape, (1, 2))

    def _test_type_check_list_mean(self):
        input1 = [1, 2]
        output1 = type_check(input1, 1, 2)
        self.assertEqual(output1.shape, (1, 2))

    def test_type_check_list_cov(self):
        input1 = [[1, 2], [2, 4]]
        output1 = type_check(input1, 2, 2)
        self.assertEqual(output1.shape, (2, 2))

    def test_type_check_array_cov(self):
        input1 = np.array([[1, 2], [2, 4]])
        output1 = type_check(input1, 2, 2)
        self.assertEqual(output1.shape, (2, 2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
