import unittest
import numpy as np
import matplotlib.pyplot as plt
import logging
from p3iv_utils_probability.distributions import *


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def plot_gaussians(gs, sigma=2, title=""):
    fig, ax = plt.subplots()
    fig.suptitle(title)

    for g in gs:
        plot_gaussian_new(g, sigma=sigma, ax=ax)
    plt.show()


def plot_gaussian_new(g, sigma=2, ax=None):
    color = np.random.rand(
        sigma + 1,
    )

    x = np.arange(len(g.mean))
    ax.plot(x, g.mean, linestyle="--", color=color)

    for s in range(1, sigma + 1):
        upper_bound = g.upper_bound(s)
        lower_bound = g.lower_bound(s)

        valid_ = upper_bound > lower_bound
        ax.fill_between(x[valid_], lower_bound[valid_], upper_bound[valid_], facecolors=color, alpha=0.3)


class TestBasics(unittest.TestCase):
    def test_univariate_float(self):
        m = 1.0
        v = 5.0
        test = UnivariateNormalDistribution(mean=m, covariance=v)
        r = test.range(2)
        self.assertEqual(r.shape, (2,))
        self.assertAlmostEqual(np.sum(r - np.array([-9.0, 11.0])), 0.0)
        self.assertAlmostEqual(test.pdf(2), 0.161434225872)
        self.assertAlmostEqual(test.cdf(1), 0.5)

    def test_truncated_univariate_float(self):
        m = 1.0
        v = 5.0
        test = TruncatedUnivariateNormalDistribution(mean=m, covariance=v, lower_truncation=0, upper_truncation=4)
        r = test.range(2)
        self.assertAlmostEqual(np.sum(r - np.array([0.0, 4.0])), 0.0)

    def test_univariate_array(self):
        m = np.array([1])
        v = np.array([5])
        test = UnivariateNormalDistribution(mean=m, covariance=v)
        r = test.range(2)
        self.assertEqual(r[1], np.array([11.0]))
        self.assertEqual(r[0], np.array([-9.0]))

    def test_univariate_seq(self):

        test = UnivariateNormalDistributionSequence()
        test.resize(100)
        test.mean = np.arange(100)
        test.covariance = np.linspace(0.1, 10, 100)
        t = test[:5]
        r = t.range(2)
        upper = r[:, 1]
        lower = r[:, 0]
        self.assertAlmostEqual(np.sum(upper - np.asarray([0.2, 1.4, 2.6, 3.8, 5.0])), 0.0)
        self.assertAlmostEqual(np.sum(lower - np.asarray([-0.2, 0.6, 1.4, 2.2, 3.0])), 0.0)
        title = "UnivariateNormalDistributionSequence"
        # plot_gaussians([test], sigma=3, title=title)

    def test_univariate_seq_append(self):
        title = "UnivariateNormalDistributionSequence"
        test = UnivariateNormalDistributionSequence()
        test.resize(50)
        test.mean = np.arange(50)
        test.covariance = np.linspace(0.1, 10, 50)

        test2 = UnivariateNormalDistributionSequence()
        test2.resize(50)
        test2.mean = np.arange(50, 100)
        test2.covariance = np.linspace(0.1, 10, 50)
        test.append(test2)

        t = test[:5]
        r = t.range(2)
        upper = r[:, 1]
        lower = r[:, 0]
        self.assertAlmostEqual(np.sum(t.mean - np.asarray([0, 1, 2, 3, 4])), 0.0)
        self.assertAlmostEqual(
            np.sum(t.covariance - np.asarray([0.1, 0.30204082, 0.50408163, 0.70612245, 0.90816327])), 0.0
        )

        self.assertAlmostEqual(np.sum(upper - np.asarray([0.2, 1.60408163, 3.00816327, 4.4122449, 5.81632653])), 0.0)
        self.assertAlmostEqual(np.sum(lower - np.asarray([-0.2, 0.39591837, 0.99183673, 1.5877551, 2.18367347])), 0.0)
        # plot_gaussians([test], sigma=3, title=title)

    def test_bivariate(self):
        m = np.array([[1, 2]])
        v = np.array([[5, 0], [0, 1]])
        test = BivariateNormalDistribution(mean=m, covariance=v)
        r = test.range(2)
        self.assertAlmostEqual(np.sum(r - np.asarray([1.0, 2.0, 0.0, 4.47213595, 2.0])), 0.0)

        x = (1.5, 3, 4)
        y = (3, 1, 5)
        self.assertAlmostEqual(np.sum(test.pdf(x, y) - np.asarray([0.0421047, 0.02893811, 0.00032147])), 0.0)
        self.assertAlmostEqual(test.cdf(1, 2), 0.25)

    def test_truncated_bivariate(self):
        m = np.array([[1, 2]])
        v = np.array([[5, 0], [0, 1]])
        tr_up = np.array([[7, 1], [4, 4]])
        tr_lw = np.array([[0, 0], [0, 0]])
        test = TruncatedBivariateNormalDistribution(
            mean=m, covariance=v, upper_truncation=tr_up, lower_truncation=tr_lw
        )

    def test_bivariate_seq(self):
        title = "BivariateNormalDistributionSequence"
        m = np.array([[1, 0], [2, 2], [3, 3]])
        v = np.array([[[5, 0], [0, 1]], [[3, 0], [0, 3]], [[1, 0], [0, 1]]])

        test = BivariateNormalDistributionSequence()
        test.resize(3)
        test.mean = m
        test.covariance = v
        r = test.range(2)
        self.assertAlmostEqual(np.sum(r[0] - np.asarray([1.0, 0.0, 0.0, 4.47213595, 2.0])), 0.0)
        self.assertAlmostEqual(np.sum(r[1] - np.asarray([2.0, 2.0, 0.0, 3.46410162, 3.46410162])), 0.0)
        self.assertAlmostEqual(np.sum(r[2] - np.asarray([3.0, 3.0, 0.0, 2.0, 2.0])), 0.0)

    def test_bivariate_seq_mean(self):
        title = "BivariateNormalDistributionSequence"
        m = np.array([[1, 0], [2, 2], [3, 3]])

        test = BivariateNormalDistributionSequence()
        test.resize(3)
        test.mean = m
        t = test[1:]
        r = t.range(2)
        truth = np.asarray([[2.0, 2.0, 0.0, 0.0, 0.0], [3.0, 3.0, 0.0, 0.0, 0.0]])
        for i, t in enumerate(truth):
            self.assertAlmostEqual(np.sum(r[i] - t), 0.0)

    def test_bivariate_seq_append(self):
        title = "BivariateNormalDistributionSequence"

        m = np.array([[1, 0], [2, 2], [3, 3]])
        v = np.array([[[5, 0], [0, 1]], [[3, 0], [0, 3]], [[1, 0], [0, 1]]])

        test1 = BivariateNormalDistributionSequence()
        test1.resize(3)
        test1.mean = m
        test1.covariance = v

        test2 = BivariateNormalDistributionSequence()
        test2.resize(3)
        test2.mean = m
        test2.covariance = v

        test1.append(test2)
        upper = test1.range(2)

        truth = np.asarray(
            [
                [1.0, 0.0, 0.0, 4.47213595, 2.0],
                [2.0, 2.0, 0.0, 3.46410162, 3.46410162],
                [3.0, 3.0, 0.0, 2.0, 2.0],
                [1.0, 0.0, 0.0, 4.47213595, 2.0],
                [2.0, 2.0, 0.0, 3.46410162, 3.46410162],
                [3.0, 3.0, 0.0, 2.0, 2.0],
            ]
        )
        for i, t in enumerate(truth):
            self.assertAlmostEqual(np.sum(upper[i] - t), 0.0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
