import numpy as np
import operator
from scipy.special import erf
from p3iv_utils_probability.distributions.base import NormalDistribution


class UnivariateNormalDistribution(NormalDistribution):
    """
    @brief Bivariate Normal Distribution
    """

    dim = 1

    def __init__(self, *args, **kwargs):
        if "covariance" not in kwargs:
            kwargs["covariance"] = np.zeros(1)
        super(UnivariateNormalDistribution, self).__init__(dim=1, *args, **kwargs)

    def __add__(self, other):
        """The distribution of the sum of two random variables with independent normal distributions.
        Reference: https://en.wikipedia.org/wiki/Sum_of_normally_distributed_random_variables
        if
        X ~ N(mu_X, sigma_X^2)
        Y ~ N(mu_Y, sigma_Y^2)
        Z = X + Y
        then
        Z ~ N(mu_X + mu_Y, sigma_X^2 + sigma_Y^2)
        """
        if isinstance(other, (int, float)):
            temp_mean = self.mean + other
            return UnivariateNormalDistribution(mean=temp_mean, covariance=self.covariance)
        elif isinstance(other, UnivariateNormalDistribution):
            temp_mean = self.mean + other.mean
            temp_cov = self.covariance + other.covariance
            return UnivariateNormalDistribution(mean=temp_mean, covariance=temp_cov)

    def __sub__(self, other):
        """The distribution of the difference of two random variables with independent normal distributions.
        Reference: https://mathworld.wolfram.com/NormalDifferenceDistribution.html
        if X ~ N(mu_X, sigma_X^2)
        Y ~ N(mu_Y, sigma_Y^2)
        Z = X - Y
        then
        Z ~ N(mu_X - mu_Y, sigma_X^2 + sigma_Y^2)
        """
        if isinstance(other, (int, float)):
            temp_mean = self.mean - other
            return UnivariateNormalDistribution(mean=temp_mean, covariance=self.covariance)
        elif isinstance(other, UnivariateNormalDistribution):
            temp_mean = self.mean - other.mean
            temp_cov = self.covariance + other.covariance
            return UnivariateNormalDistribution(mean=temp_mean, covariance=temp_cov)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            temp_mean = self.mean * other
            return UnivariateNormalDistribution(mean=temp_mean, covariance=self.covariance)
        elif isinstance(other, UnivariateNormalDistribution):
            temp_mean = (self.mean * other.covariance + other.mean * self.covariance) / (
                self.covariance + other.covariance
            )
            temp_cov = np.sqrt((self.covariance * other.covariance) / (self.covariance + other.covariance))
            return UnivariateNormalDistribution(mean=temp_mean, covariance=temp_cov)

    def __div__(self, other):
        # todo
        pass

    def pdf(self, x, *args):
        mu = self.mean
        sigma = np.sqrt(self.covariance)
        f_val = 1 / (np.sqrt(2 * np.pi) * sigma) * np.exp(-((x - mu) ** 2 / (2 * sigma ** 2)))
        return f_val

    def cdf(self, x, *args):
        mu = self.mean[0]
        sigma = np.sqrt(self.covariance)
        f_val = 1 / 2 * (1 + erf((x - mu) / (sigma * np.sqrt(2))))
        return f_val

    def range(self, n_std):
        return np.squeeze([self.mean - self.covariance * n_std, self.mean + self.covariance * n_std])
