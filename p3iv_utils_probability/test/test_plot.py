import unittest
import logging
import numpy as np
import matplotlib.pyplot as plt
from p3iv_utils_probability.distributions import (
    UnivariateNormalDistribution,
    BivariateNormalDistribution,
    UnivariateNormalDistributionSequence,
)
from p3iv_utils_probability.visualization.plot_distribution import PlotProbabilityDistribution


class TestUnivariateNormalDistribution(unittest.TestCase):
    def test_bivariate_normal_ellipse(self):
        m = np.array([1, 2])
        v = np.array([[3, -2], [-2, 3]])
        dist = BivariateNormalDistribution(mean=m, covariance=v)
        plot = PlotProbabilityDistribution()
        fig = plt.figure(figsize=(5, 5))
        ax0 = fig.add_subplot(111)
        plot(ax0, dist)
        ax0.set_aspect("equal")
        ax0.set_xlim(-7.5, 7.5)
        ax0.set_ylim(-7.5, 7.5)
        ax0.legend()
        plt.show()

    def test_bivariate_normal_ellipse_only(self):
        m = np.array([1, 2])
        v = np.array([[3, -2], [-2, 3]])
        dist = BivariateNormalDistribution(mean=m, covariance=v)
        plot = PlotProbabilityDistribution()
        fig = plt.figure(figsize=(5, 5))
        ax0 = fig.add_subplot(111)
        plot.plot_bivariate_pdf_confidence_ellipse(ax0, dist)
        ax0.set_aspect("equal")
        ax0.set_xlim(-7.5, 7.5)
        ax0.set_ylim(-7.5, 7.5)
        ax0.legend()
        plt.show()

    def test_bivariate_normal_circle(self):
        m = np.array([1, 2])
        v = np.array([[3, 0], [0, 3]])
        dist = BivariateNormalDistribution(mean=m, covariance=v)
        plot = PlotProbabilityDistribution()
        fig = plt.figure(figsize=(5, 5))
        ax0 = fig.add_subplot(111)
        plot(ax0, dist)
        ax0.set_aspect("equal")
        ax0.set_xlim(-7.5, 7.5)
        ax0.set_ylim(-7.5, 7.5)
        ax0.legend()
        plt.show()

    def test_univariate_normal_sequence(self):
        dist = UnivariateNormalDistributionSequence()
        dist.resize(50)
        dist.mean = np.arange(50)
        dist.covariance = np.linspace(0.1, 10, 50)
        plot = PlotProbabilityDistribution()
        fig = plt.figure()
        ax0 = fig.add_subplot(111)
        plot(ax0, dist)
        ax0.set_xlim(0, 50)
        ax0.set_ylim(0, 100)
        ax0.legend()
        plt.show()

    def test_univariate_normal_sequence_fine(self):
        dist = UnivariateNormalDistributionSequence()
        dist.resize(500)
        dist.mean = np.linspace(0.0, 50, 500)
        dist.covariance = np.linspace(0.1, 10, 500)
        plot = PlotProbabilityDistribution()
        fig = plt.figure()
        ax0 = fig.add_subplot(111)
        plot(ax0, dist)
        ax0.set_xlim(0, 50)
        ax0.set_ylim(0, 10)
        ax0.legend()
        plt.show()

    def test_truncated_univariate_normal_sequence(self):
        dist = UnivariateNormalDistributionSequence()
        dist.resize(50)
        dist.mean = np.arange(50)
        dist.covariance = np.linspace(0.1, 10, 50)
        plot = PlotProbabilityDistribution()
        fig = plt.figure()
        ax0 = fig.add_subplot(111)
        plot(ax0, dist)
        ax0.set_xlim(0, 50)
        ax0.set_ylim(0, 100)
        ax0.legend()
        plt.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
