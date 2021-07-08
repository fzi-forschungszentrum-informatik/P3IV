# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import unittest
import logging
import numpy as np
from scipy.stats import multivariate_normal
from p3iv_utils_probability.distributions import UnivariateNormalDistribution, BivariateNormalDistribution


class TestUnivariateNormalDistribution(unittest.TestCase):
    def setUp(self):
        m = 1.0
        v = 5.0
        self.distribution = UnivariateNormalDistribution(mean=m, covariance=v)
        self.dist2compare = multivariate_normal(m, v)

    def test_bounds_float(self):
        self.assertAlmostEqual(np.sum(self.distribution.range(-2) - np.asarray([11, -9])), 0.0)
        self.assertAlmostEqual(np.sum(self.distribution.range(2) - np.asarray([-9, 11])), 0.0)

    def test_pdf_and_cdf_float(self):
        val = 2.0
        self.assertAlmostEqual(self.distribution.pdf(val)[0], self.dist2compare.pdf(val), places=4)
        self.assertAlmostEqual(self.distribution.cdf(val)[0], self.dist2compare.cdf(val), places=4)

    def test_pdf_and_cdf_array(self):
        vals = np.array([-1, -0.5, 0, 1, 2, 3, 4, 5])
        pdf_diffs = self.distribution.pdf(vals) - self.dist2compare.pdf(vals)
        cdf_diffs = self.distribution.cdf(vals) - self.dist2compare.cdf(vals)
        for i in range(len(vals)):
            self.assertAlmostEqual(pdf_diffs[i], 0.0, places=4)
            self.assertAlmostEqual(cdf_diffs[i], 0.0, places=4)

    def test_sum_and_sub(self):
        m_2 = 2.0
        v_2 = 3.0
        distribution_2 = UnivariateNormalDistribution(mean=m_2, covariance=v_2)
        sum_distr = self.distribution + distribution_2
        sub_distr = self.distribution - distribution_2
        self.assertIsInstance(sum_distr, UnivariateNormalDistribution)
        self.assertIsInstance(sub_distr, UnivariateNormalDistribution)
        self.assertEqual(sum_distr.mean, 3)
        self.assertAlmostEqual(sum_distr.covariance, 8)

        sum_distr_c = self.distribution + 2.5
        sub_distr_c = self.distribution - 3
        self.assertEqual(sum_distr_c.mean[0], 3.5)
        self.assertEqual(sub_distr_c.mean[0], -2)
        self.assertEqual(sum_distr_c.covariance, self.distribution.covariance)
        self.assertEqual(sub_distr_c.covariance, self.distribution.covariance)

    def test_mul(self):
        m_2 = 2.0
        v_2 = 3.0
        distribution_2 = UnivariateNormalDistribution(mean=m_2, covariance=v_2)
        mul_distr = self.distribution * distribution_2
        self.assertIsInstance(mul_distr, UnivariateNormalDistribution)
        self.assertAlmostEqual(mul_distr.mean, (1.0 * 3.0 + 2.0 * 5.0) / 8.0)
        self.assertAlmostEqual(mul_distr.covariance, np.sqrt((5.0 * 3.0) / (5.0 + 3.0)))


class TestBivariateNormalDistribution(unittest.TestCase):
    def setUp(self):
        m = np.array([[1, 2]])
        v = np.array([[5, 1], [1, 1]])
        try:
            self.distribution = BivariateNormalDistribution(mean=m, covariance=v)
            self.assertTrue(False)
        except AssertionError:
            # AssertionError is expected
            m = np.array([1, 2])
            self.distribution = BivariateNormalDistribution(mean=m, covariance=v)
            self.dist2compare = multivariate_normal(m, v)

    def test_pdf_and_cdf_xy(self):
        x = 1
        y = 2
        pdf_diffs = self.distribution.pdf(x, y) - self.dist2compare.pdf([x, y])
        cdf_diffs = self.distribution.cdf(x, y) - self.dist2compare.cdf([x, y])

        self.assertAlmostEqual(pdf_diffs, 0.0, places=4)
        self.assertAlmostEqual(cdf_diffs, 0.0, places=4)

    def test_bounds(self):
        res = self.distribution.range(2)
        gt = np.array([1, 2, 0.23182380450040307, 4.576491222541474, 1.7480640977952844])
        diff = np.asarray(res) - gt
        for d in diff:
            self.assertAlmostEqual(d, 0.0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
