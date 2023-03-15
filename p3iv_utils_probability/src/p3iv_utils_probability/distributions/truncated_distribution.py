# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
from scipy.special import erf
import scipy.integrate as integrate
from p3iv_utils_probability.distributions.base import TruncatedNormalDistribution
from p3iv_utils_probability.distributions.univariate_distribution import UnivariateNormalDistribution
from p3iv_utils_probability.distributions.bivariate_distribution import BivariateNormalDistribution


class TruncatedUnivariateNormalDistribution(TruncatedNormalDistribution, UnivariateNormalDistribution):
    """
    @brief Truncated Univariate Normal Distribution
    """

    def __init__(self, *args, **kwargs):
        super(TruncatedUnivariateNormalDistribution, self).__init__(1, *args, **kwargs)

    @property
    def mean(self):
        """Calculate the mean of the truncated normal distribution"""
        mu, sigma, alpha, beta, Z = self._intermediate_parameters()
        truncated_mean = mu + (self._pdf_standard(alpha) - self._pdf_standard(beta)) * sigma / Z
        return truncated_mean

    def pdf(self, x, n_std=None, *args):
        mu, sigma, alpha, beta, Z = self._intermediate_parameters()
        xi = (x - mu) / sigma
        raw_density = np.asarray((1 / sigma) * self._pdf_standard(xi) / Z)
        # approximated normal distribution may return positive pdfs beyond truncation borders
        # eliminate these with a filter that is a numpy-array of boolean values
        booleans = self.within_boundary(x, n_std)
        return raw_density * booleans

    def cdf(self, x, n_std=None, *args):
        mu, sigma, alpha, beta, Z = self._intermediate_parameters()
        xi = (x - mu) / sigma
        raw_cumulative_density = np.asarray((self._cdf_standard(xi) - self._cdf_standard(alpha)) / Z)
        # approximated normal distribution may return positive pdfs beyond truncation borders
        # eliminate these with a filter that is a numpy-array of boolean values
        booleans = self.within_boundary(x, n_std)
        return raw_cumulative_density * booleans

    def range(self, n_std):
        r = super(TruncatedUnivariateNormalDistribution, self).range(n_std)
        upper_bound = r[1]
        if self._upper_truncation_bound is not None:
            upper_bound = np.clip(upper_bound, self._lower_truncation_bound, self._upper_truncation_bound)

        lower_bound = r[0]
        if self._lower_truncation_bound is not None:
            lower_bound = np.clip(lower_bound, self._lower_truncation_bound, self._upper_truncation_bound)
        return [lower_bound, upper_bound]

    def within_boundary(self, x, n_std):
        if n_std:
            r = self.range(n_std)
            self._lower_truncation_bound, self._upper_truncation_bound = r

        if isinstance(x, (int, float)):
            return (x >= self._lower_truncation_bound) & (x <= self._upper_truncation_bound)
        else:
            x = np.asarray(x)
            return (x >= self._lower_truncation_bound) & (x <= self._upper_truncation_bound)

    def _intermediate_parameters(self):
        """Calculate intermediate parameters that are defined on Wikipedia [1].
        alpha: (lower_bound - original_mean) / stddev
        beta: (upper_bound - original_mean) / stddev
        Z: available "range" of CDF of the truncated interval
        [1] https://en.wikipedia.org/wiki/Truncated_normal_distribution
        """
        sigma = np.sqrt(self.covariance.flatten()[0])
        mu = self._mean.flatten()[0]

        alpha = (self._lower_truncation_bound - mu) / sigma
        beta = (self._upper_truncation_bound - mu) / sigma
        Z = self._cdf_standard(beta) - self._cdf_standard(alpha)
        return mu, sigma, alpha, beta, Z

    @staticmethod
    def _pdf_standard(x):
        """Probability distribution of standard normal distribution"""
        return 1 / np.sqrt(2 * np.pi) * np.exp(-(x**2) / 2)

    @staticmethod
    def _cdf_standard(x):
        """Cumulative distribution function of standard normal distribution"""
        return 1 / 2 * (1 + erf(x / np.sqrt(2)))


class TruncatedBivariateNormalDistribution(TruncatedNormalDistribution, BivariateNormalDistribution):
    """
    @brief Truncated Bivariate Normal Distribution
    Use with care! Implementations are experimental to some part!
    """

    def __init__(self, *args, **kwargs):
        super(TruncatedBivariateNormalDistribution, self).__init__(2, *args, **kwargs)

    def within_n_std(self, x, y, n_std):
        """Return the Bool value if a point is within the n_std * deviation range."""
        points = self.reform_points(x, y)

        mean_x, mean_y, theta, a, b = super(TruncatedBivariateNormalDistribution, self).range(n_std)
        c = np.sqrt(a**2 - b**2)  # calculate linear eccentricity
        F1 = np.array([mean_x, mean_y]) + c * np.array([np.cos(theta), np.sin(theta)])  # focal-point 1 coords
        F2 = np.array([mean_x, mean_y]) - c * np.array([np.cos(theta), np.sin(theta)])  # focal-point 2 coords

        PF1 = np.subtract(points, F1)  # |PF1|
        PF2 = np.subtract(points, F2)  # |PF2|
        dist = np.linalg.norm(PF1, axis=1) + np.linalg.norm(PF2, axis=1)  # |PF1| + |PF2|
        return dist <= 2 * a

    def within_boundary(self, x, y, n_std=None):
        # todo: implement range based on ellipses.
        if n_std:
            warnings.warn("Not implemented yet")

        points = self.reform_points(x, y)
        bool_matrix = (points >= self._lower_truncation_bound) & (points <= self._upper_truncation_bound)
        # if one of the coordinates is not within the boundaries, the point is not within the boundaries.
        bool_list = bool_matrix[:, 0] * bool_matrix[:, 1]
        return bool_list

    @staticmethod
    def reform_points(x, y):
        x = np.asarray(x)
        y = np.asarray(y)
        points = np.dstack([x, y]).reshape(-1, 2)
        return points

    @staticmethod
    def type_guard(val):
        if isinstance(val, list):
            return np.asarray(val)
        elif isinstance(val, (int, float)):
            return np.asarray([val])
        elif isinstance(val, np.ndarray):
            return val
        else:
            raise TypeError

    def pdf(self, x, y, n_std=None, mesh_range=False, *args):
        x = self.type_guard(x)
        y = self.type_guard(y)
        if mesh_range:
            x_ = np.linspace(x - mesh_range, x + mesh_range, 500)
            y_ = np.linspace(y - mesh_range, y + mesh_range, 500)
            X, Y = np.meshgrid(x_, y_)
            points = np.dstack([X, Y]).reshape(-1, 2)
            # if one of the coordinates is not within the boundaries, the point is not within the boundaries.
            booleans = np.all(
                (points >= self._lower_truncation_bound) & (points <= self._upper_truncation_bound), axis=1
            )
            booleans = booleans.reshape(len(x) * 500, len(y) * 500)
            return self._pdf(X, Y) * booleans
        else:
            booleans = True
            return self._pdf(x, y) * booleans

    def cdf(self, x, y, n_std=None, *args):
        x = self.type_guard(x)
        y = self.type_guard(y)
        upper_x, upper_y = self._upper_truncation_bound
        lower_x, lower_y = self._lower_truncation_bound

        integration_interval = np.asarray(
            [[np.ones_like(x) * lower_x, np.minimum(x, upper_x)], [np.ones_like(x) * lower_y, np.minimum(y, upper_y)]]
        )

        # using pdf in range n_std
        # cumulated_density = integrate.nquad(lambda x_, y_: self.pdf(x_, y_), integration_interval)[0]
        _, _, l = integration_interval.shape
        cumulated_density = np.empty(l)
        for i in range(l):
            interval = integration_interval[:, :, i]
            cumulated_density[i] = integrate.nquad(self._pdf, interval)[0]

        return cumulated_density

    """
    def pdf(self, x, y, n_std=None, mesh_range=False, *args):
        if mesh_range:
            X, Y = np.meshgrid(x, y)
            range_filter = self.within_boundary(X, Y, n_std).reshape(len(x), len(y))
            try:
                boundary_filter = self.within_boundary(X, Y).reshape(len(x), len(y))
                filter = boundary_filter * range_filter
            except:
                filter = range_filter

        else:
            range_filter = self.within_boundary(x, y, n_std)
            try:
                boundary_filter = self.within_boundary(x, y)
                filter = boundary_filter * range_filter
            except:
                print("No boundary specified.")
                filter = range_filter

        return super(TruncatedBivariateNormalDistribution, self).pdf(x, y, mesh_range=mesh_range) * filter

    def cdf(self, x_lim, y_lim, n_std=None, *args):
        upper_x = self._upper_truncation_bound[0, 0]
        upper_y = self._upper_truncation_bound[0, 1]
        lower_x = self._lower_truncation_bound[0, 0]
        lower_y = self._lower_truncation_bound[0, 1]
        print("lower_x, upper_x, lower_y, upper_y = {}".format([lower_x, upper_x, lower_y, upper_y]))
        if (x_lim < self._lower_truncation_bound[0, 0]) or (y_lim < self._lower_truncation_bound[0, 1]):
            return 0
        else:
            integrate_region = [[lower_x, min(x_lim, upper_x)], [lower_y, min(y_lim, upper_y)]]
            print("integrate_region = {}".format(integrate_region))

            # using not truncated pdf
            # cumulated_density = integrate.nquad(lambda x, y: super(TruncatedBivariateNormalDistribution, self).pdf(x, y), integrate_region)[0]

            # using pdf in range n_std
            cumulated_density = integrate.nquad(lambda x, y: self.pdf(x, y), integrate_region)[0]

            return cumulated_density
    """
