import unittest
import logging
import numpy as np
from util_probability.distributions import TruncatedUnivariateNormalDistribution, TruncatedBivariateNormalDistribution


class TestTruncatedUnivariateNormalDistribution(unittest.TestCase):
    def setUp(self):
        m = 1.0
        v = 5.0
        self.distribution = TruncatedUnivariateNormalDistribution(
            mean=m, covariance=v, lower_truncation=0, upper_truncation=4
        )

    def test_bounds_float(self):
        lower, upper = self.distribution.range(2)
        print(("\nUpper bound : {}\n".format(upper)))
        print(("\nLower bound : {}\n".format(lower)))

    def test_pdf_and_cdf(self):
        test_list = [-1, -0.5, 0, 1, 2, 3, 4, 5]
        print(("\npdf = {}\n".format(self.distribution.pdf(test_list))))
        print(("\ncdf = {}\n".format(self.distribution.cdf(test_list))))
        test_number = 2
        print(("\npdf = {}\n".format(self.distribution.pdf(test_number))))
        print(("\ncdf = {}\n".format(self.distribution.cdf(test_number))))


class TestTruncatedBivariateNormalDistribution(unittest.TestCase):
    def setUp(self):
        m = np.array([1, 2])
        v = np.array([[5, 1], [1, 1]])
        tr_up = np.array([7, 1])
        tr_lw = np.array([0, 0])
        self.distribution = TruncatedBivariateNormalDistribution(
            mean=m, covariance=v, upper_truncation=tr_up, lower_truncation=tr_lw
        )

    def test_distribution_range(self):
        distribution_range = self.distribution.range(2)
        print(("Distribution range : \n{}\n".format(distribution_range)))

    def test_pdf_and_cdf(self):
        x = [1.5, 3, 4]
        y = [1, 3, 5]
        print(("\npdf = {}\n".format(self.distribution.pdf(x, y))))
        print(("\ncdf = {}\n".format(self.distribution.cdf(x, y))))

    def test_pdf_and_cdf_mesh(self):
        x = 2
        y = 2
        print(("\npdf = {}\n".format(self.distribution.pdf(x, y, mesh_range=10))))
        print(("\ncdf = {}\n".format(self.distribution.cdf(x, y))))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
