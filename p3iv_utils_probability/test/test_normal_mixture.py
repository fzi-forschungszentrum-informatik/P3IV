import numpy as np
import unittest
import logging
from p3iv_utils_probability.distributions import (
    UnivariateNormalMixtureDistribution,
    UnivariateNormalSequenceMixtureDistribution,
    UnivariateNormalDistributionSequence,
    TruncatedUnivariateNormalDistributionSequence,
    TruncatedUnivariateNormalSequenceMixtureDistribution,
)


class TestUnivariateNormalMixtureDistribution(unittest.TestCase):
    def setUp(self):
        m = np.array([10, 20])
        v = np.array([1, 2])
        w = np.array([0.5, 0.5])
        self.distribution = UnivariateNormalMixtureDistribution(weights=w, mean=m, covariance=v)

    def test_distribution_range(self):
        lw, up = self.distribution.range(2)
        print(("Distribution range : \n{}\n".format(lw)))
        print(("Distribution range : \n{}\n".format(up)))

    def test_init_false_weights(self):
        try:
            m = np.array([10, 20])
            v = np.array([1, 2])
            w = np.array([0.3, 0.5])  # must cause error; weights must sum up to 1
            distribution = UnivariateNormalMixtureDistribution(weights=w, mean=m, covariance=v)
        except:
            pass

    def test_init_single_weights(self):
        m = np.array([10])
        v = np.array([12])
        w = np.array([1.0])
        distribution = UnivariateNormalMixtureDistribution(weights=w, mean=m, covariance=v)
        distribution.means = m
        print(distribution)
        print("Bound  ", distribution.range(2))
        # plot_gaussians(distribution.components, sigma=3, title='UnivariateNormalMixtureDistribution - single')

    def test_init_high_dim(self):
        m = np.array([10, 20])
        v = np.array([1, 2])
        w = np.array([0.5, 0.5])
        mog = UnivariateNormalMixtureDistribution(weights=w, mean=m, covariance=v)
        print(mog)
        print("Bound")
        print(mog.range(2))

        m[0] = 0
        mog.means = m
        print(mog)
        print("Bound")
        print(mog.range(2))


class TestTruncatedUnivariateNormalMixtureDistribution(unittest.TestCase):
    def setUp(self):
        m = np.array([10, 20])
        v = np.array([1, 2])
        w = np.array([0.5, 0.5])
        self.distribution = UnivariateNormalSequenceMixtureDistribution(weights=w, mean=m, covariance=v)


class TestUnivariateNormalSequenceMixtureDistribution(unittest.TestCase):
    def test_init_components(self):
        m1 = np.arange(100)
        v1 = np.linspace(0.1, 10, 100)
        tg1 = UnivariateNormalDistributionSequence()
        tg1.resize(100)
        tg1.mean = m1
        tg1.covariance = v1
        w_1 = 0.3

        m2 = np.arange(100, 200)
        v2 = np.linspace(0.1, 10, 100)
        tg2 = UnivariateNormalDistributionSequence()
        tg2.resize(100)
        tg2.mean = m2
        tg2.covariance = v2
        w_2 = 0.7

        tgs = [tg1, tg2]
        ws = [w_1, w_2]
        mog = UnivariateNormalSequenceMixtureDistribution(weights=ws, components=tgs)

        # plot_gaussians(mog.components, sigma=3, title="Mixture w. init UnivariateNormalSequenceDistribution(s)")


class TestTruncatedUnivariateNormalSequenceMixtureDistribution(unittest.TestCase):
    def setUp(self):
        pass

    """
    def test_truncated_univariate_sequence_init_two_arrays(self):
        m = np.array([np.arange(100), np.arange(100) * 2])
        v = np.vstack([np.linspace(0.1, 10, 100)]*2)

        tr_up_1 = np.ones(100) * 100
        tr_up_2 = np.ones(100) * 80
        tr_up = np.vstack([tr_up_1, tr_up_2])

        tr_lw_1 = np.ones(100) * 30
        tr_lw_2 = np.ones(100) * 20
        tr_lw = np.vstack([tr_lw_1, tr_lw_2])

        w = np.array([0.5, 0.5])

        mog = TruncatedUnivariateNormalSequenceMixtureDistribution(tr_up, tr_lw, weights=w, mean=m, covariance=v)
        print mog
        print mog.distribution_range(2)

        plot_gaussians(mog.components, sigma=3, title='TruncatedUnivariateSequence init two arrays')

    def test_truncated_univariate_sequence(self):
        m = np.arange(15).reshape(3, 5) * 100
        v = np.ones((3, 5)) * 20
        w = np.ones(3) / 3

        # tr = np.ones((3, 5)) * 99
        tr_up = np.ones((3, 5))
        tr_up[0, :] *= 350
        tr_up[1, :] *= 800
        tr_up[2, :] *= 1300

        tr_lw = np.ones((3, 5))
        tr_lw[0, :] *= 250
        tr_lw[1, :] *= 500
        tr_lw[2, :] *= 1100

        mog = TruncatedUnivariateNormalSequenceMixtureDistribution(tr_up, tr_lw, weights=w, mean=m, covariance=v)
        print mog
        print "truncation_array up:"
        print tr_up
        print "truncation_array low:"
        print tr_lw

        plot_gaussians(mog.components, sigma=3, title='TruncatedUnivariateSequence init three arrays')

    def test_truncated_univariate_sequence_no_boundaries(self):
        m = np.arange(15).reshape(3, 5) * 100
        v = np.ones((3, 5)) * 20
        w = np.ones(3) / 3

        # tr = np.ones((3, 5)) * 99
        tr_up = np.asarray([None]*3)
        tr_lw = np.asarray([None]*3)

        mog = TruncatedUnivariateNormalSequenceMixtureDistribution(tr_up, tr_lw, weights=w, mean=m, covariance=v)
        print mog
        print "truncation_array up:"
        print tr_up
        print "truncation_array low:"
        print tr_lw

        plot_gaussians(mog.components, sigma=3, title='3 (not truncated) Univariate Normal Sequence Mixture')

    def test_init_components(self):
        m1 = np.arange(100)
        v1 = np.linspace(0.1, 10, 100)
        tr_upper1 = np.ones(100) * 80
        tr_lower1 = np.ones(100) * 30
        tg1 = TruncatedUnivariateNormalSequenceDistribution(tr_upper1, tr_lower1, mean=m1, covariance=v1)
        w_1 = 0.3

        m2 = np.arange(100)
        v2 = np.linspace(0.1, 10, 100)
        tr_upper2 = np.ones(100) * 70
        tr_lower2 = np.ones(100) * 40
        tg2 = TruncatedUnivariateNormalSequenceDistribution(tr_upper2, tr_lower2, mean=m2, covariance=v2)
        w_2 = 0.7

        tgs = [tg1, tg2]
        ws = [w_1, w_2]
        mog = UnivariateNormalSequenceMixtureDistribution(weights=ws, components=tgs)

        plot_gaussians(mog.components, sigma=3, title="Mixture w. init TruncatedUnivariateNormalSequenceDistribution(s)")

    """


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
