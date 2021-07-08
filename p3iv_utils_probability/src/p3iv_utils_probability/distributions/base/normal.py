# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import operator
import numpy as np
from p3iv_utils_probability.distributions.base.probability_distribution import ProbabilityDistribution


def type_check(obj, row, col):
    if isinstance(obj, list):
        obj = np.asarray(obj)
    elif isinstance(obj, (int, np.integer, float, np.floating)):
        obj = np.asarray([obj])
    assert isinstance(obj, np.ndarray)

    if obj.shape == (1,):
        obj = np.expand_dims(obj, axis=1)

    elif obj.shape == (2,):
        obj = np.expand_dims(obj, axis=0)

    assert obj.shape == (row, col)
    return obj


def check_covariance_vals(cov, dimension):
    if dimension == 1:
        assert np.all(cov >= 0)
    elif dimension == 2:
        assert np.all(cov.diagonal() >= 0)
        assert cov[0, 1] == cov[1, 0]
        if np.any(cov.diagonal() == 0):
            assert cov[0, 1] == 0
        else:
            rho = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
            assert (rho > -1) & (rho < 1)


class NormalDistribution(ProbabilityDistribution):
    """
    @brief Normal Distribution
    """

    def __init__(self, dim, *args, **kwargs):

        super(NormalDistribution, self).__init__(*args, **kwargs)
        self._dim = dim

        # initialize mean
        if "mean" in kwargs and kwargs["mean"] is not None:
            mean = type_check(kwargs["mean"], 1, self._dim)
            self._mean = mean
        else:
            self._mean = np.empty([1, self._dim])

        # initialize covariance
        if "covariance" in kwargs and kwargs["covariance"] is not None:
            covariance = type_check(kwargs["covariance"], self._dim, self._dim)
            check_covariance_vals(covariance, self._dim)
            self._covariance = covariance
        else:
            self._covariance = np.zeros([self._dim, self._dim])

    def __repr__(self):
        return "Mean:\n%s\nCoVariance:\n%s\n\n" % (str(self._mean), str(self._covariance))

    """
    # todo!
    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass
    """

    @property
    def dim(self):
        return self._dim

    @property
    def mean(self):
        return self._mean[-1]

    @mean.setter
    def mean(self, mean):
        self._mean = mean = type_check(mean, 1, self._dim)

    @property
    def covariance(self):
        return self._covariance[-1]

    @covariance.setter
    def covariance(self, cov):
        check_covariance_vals(cov, self._dim)
        self._covariance = type_check(cov, self._dim, self._dim)


class TruncatedNormalDistribution(NormalDistribution):
    def __init__(self, dim, *args, **kwargs):

        super(TruncatedNormalDistribution, self).__init__(*args, **kwargs)

        if "upper_truncation" in kwargs:
            self._upper_truncation_bound = np.asarray(kwargs["upper_truncation"])
        else:
            self._upper_truncation_bound = np.asarray([np.inf] * dim)

        if "lower_truncation" in kwargs:
            self._lower_truncation_bound = np.asarray(kwargs["lower_truncation"])
        else:
            self._lower_truncation_bound = np.asarray([-np.inf] * dim)

        assert np.all(self._lower_truncation_bound <= self._upper_truncation_bound)

    def __repr__(self):
        return "Mean:\n%s\nCoVariance:\n%s\nUpperTruncation:\n%s\nLowerTruncation:\n%s\n\n" % (
            str(self._mean),
            str(self._covariance),
            str(self._upper_truncation_bound),
            str(self._lower_truncation_bound),
        )

    """
    @staticmethod
    def get_truncation_indices(operator_cmp, bound, truncation_array):
        assert bound.shape[-1] == truncation_array.shape[-1]
        return np.where(operator_cmp(bound, truncation_array))
    """
