import unittest
import logging
import numpy as np
from p3iv_utils_probability.distributions.base.normal import check_covariance_vals


class TestValueCheck(unittest.TestCase):
    def setUp(self):
        self.raised = False

    def test_value_check_cov_1D_pass(self):
        cov = np.array([1])
        check_covariance_vals(cov, 1)

    def test_value_check_cov_1D_negative_raise(self):
        cov = np.array([-1])
        try:
            check_covariance_vals(cov, 1)
        except AssertionError:
            self.raised = True
        self.assertTrue(self.raised)

    def test_value_check_cov_2D_pass(self):
        cov = np.array([[3, 1], [1, 5]])
        check_covariance_vals(cov, 2)

    def test_value_check_cov_2D_negative_raise(self):
        cov = np.array([[-3, 1], [1, 5]])
        try:
            check_covariance_vals(cov, 2)
        except AssertionError:
            self.raised = True
        self.assertTrue(self.raised)

    def test_value_check_cov_2D_zero_raise(self):
        cov = np.array([[3, 1], [1, 0]])
        try:
            check_covariance_vals(cov, 2)
        except AssertionError:
            self.raised = True
        self.assertTrue(self.raised)

    def test_value_check_cov_2D_zero_pass(self):
        cov = np.array([[3, 0], [0, 0]])
        check_covariance_vals(cov, 2)

    def test_value_check_cov_2D_rho_raise(self):
        cov = np.array([[3, 4], [4, 5]])
        try:
            check_covariance_vals(cov, 2)
        except AssertionError:
            self.raised = True
        self.assertTrue(self.raised)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
