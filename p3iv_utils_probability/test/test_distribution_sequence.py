import unittest
import logging
import numpy as np
import matplotlib.pyplot as plt
from util_probability.distributions import UnivariateNormalDistributionSequence, BivariateNormalDistributionSequence
from util_probability.visualization.plot_distribution import PlotProbabilityDistribution


class TestUnivariateNormalDistributionSequence(unittest.TestCase):
    def setUp(self):
        self.distribution = UnivariateNormalDistributionSequence()
        self.distribution.resize(100)
        self.distribution.mean = np.arange(100)
        self.distribution.covariance = np.linspace(0.1, 10, 100)

    def test_slicing(self):
        d = self.distribution[:5]
        self.assertEqual(len(d), 5)

    def test_bounds_float(self):
        d = self.distribution[:5]
        self.assertEqual(len(d), 5)
        r = d.range(2)
        bound_plus_2 = r[:, 1]
        bound_minus_2 = r[:, 0]
        gt_bound_plus_2 = np.array([0.2, 1.4, 2.6, 3.8, 5.0])
        gt_bound_minus_2 = np.array([-0.2, 0.6, 1.4, 2.2, 3.0])
        diff_plus = bound_plus_2 - gt_bound_plus_2
        diff_minus = bound_minus_2 - gt_bound_minus_2
        for i in range(5):
            self.assertAlmostEqual(diff_plus[i], 0.0)
            self.assertAlmostEqual(diff_minus[i], 0.0)

    def test_plot(self):
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.set_aspect("equal")
        plot = PlotProbabilityDistribution()
        plot(ax, self.distribution, sigma=3, title="UnivariateNormalDistributionSequence")
        plt.show()


class TestUnivariateNormalDistributionSequenceAppend(unittest.TestCase):
    def setUp(self):
        dist1 = UnivariateNormalDistributionSequence()
        dist1.resize(50)
        dist1.mean = np.arange(50)
        dist1.covariance = np.linspace(0.1, 10, 50)
        self.dist1 = dist1

        dist2 = UnivariateNormalDistributionSequence()
        dist2.resize(50)
        dist2.mean = np.arange(50, 100)
        dist2.covariance = np.linspace(0.1, 10, 50)
        self.dist2 = dist2

    def test_append(self):
        self.dist1.append(self.dist2)
        self.assertEqual(len(self.dist1), 100)

    def test_plot(self):
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.set_aspect("equal")
        plot = PlotProbabilityDistribution()
        plot(ax, self.dist1, sigma=3, title="UnivariateNormalDistributionSequence - Appended")
        plt.show()


class TestBivariateNormalDistributionSequence(unittest.TestCase):
    def setUp(self):
        m = np.array([[1, 0], [2, 2], [3, 3]])
        v = np.array([[[5, 0], [0, 1]], [[3, 0], [0, 3]], [[1, 0], [0, 1]]])
        self.distribution = BivariateNormalDistributionSequence()
        self.distribution.resize(3)
        self.distribution.mean = m
        self.distribution.covariance = v

    def test_bounds_float(self):
        bound = self.distribution.range(2)
        print("Bound : \n")
        print(bound)
        result = np.array(
            [[1.0, 0.0, 0.0, 4.47213595, 2.0], [2.0, 2.0, 0.0, 3.46410162, 3.46410162], [3.0, 3.0, 0.0, 2.0, 2.0]]
        )
        self.assertAlmostEqual(np.sum(bound - result), 0.0, places=3)

    def test_append(self):
        self.distribution.append(self.distribution)
        print((self.distribution))
        self.assertEqual(len(self.distribution), 6)
        bound = self.distribution.range(2)
        print("Bound : \n")
        print((bound[:10]))


class TestBivariateNormalDistributionSequenceMeanOnly(unittest.TestCase):
    def setUp(self):
        m = np.array([[1, 0], [2, 2], [3, 3]])
        self.distribution = BivariateNormalDistributionSequence()
        self.distribution.resize(3)
        self.distribution.mean = m

    def test_bounds_float(self):
        bound = self.distribution.range(2)
        print("Bound : \n")
        print(bound)

    def test_slicing(self):
        print((self.distribution[1]))
        print((self.distribution[:2]))
        print((self.distribution))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
