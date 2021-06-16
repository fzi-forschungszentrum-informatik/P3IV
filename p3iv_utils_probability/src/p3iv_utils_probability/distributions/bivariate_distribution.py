import numpy as np
import operator
from p3iv_utils_probability.distributions.base import (
    NormalDistribution,
    TruncatedNormalDistribution,
    DistributionSequence,
    Mixture,
)
from scipy.stats import multivariate_normal
import scipy.integrate as integrate


class BivariateNormalDistribution(NormalDistribution):
    """
    @brief Bivariate Normal Distribution
    """

    dim = 2

    def __init__(self, *args, **kwargs):
        if "covariance" not in kwargs:
            kwargs["covariance"] = np.zeros([2, 2])
        super(BivariateNormalDistribution, self).__init__(dim=self.dim, *args, **kwargs)

    def pdf(self, x, y, mesh_range=0.0):
        x = np.asarray(x).reshape(-1, 1)
        y = np.asarray(y).reshape(-1, 1)
        assert x.shape == y.shape
        if mesh_range != 0.0:
            x, y = np.meshgrid(
                np.linspace(x - mesh_range, x + mesh_range, 500), np.linspace(y - mesh_range, y + mesh_range, 500)
            )

        return self._pdf(x, y)

    def cdf(self, x, y):
        return self._cdf(x, y)

    def range(self, n_std):
        x, y = self._mean[0]
        theta, ell_radius_x, ell_radius_y = self.get_ellipse_parameters(self._covariance, n_std)
        return np.asarray([x, y, theta, ell_radius_x, ell_radius_y])

    @staticmethod
    def get_ellipse_parameters(covariance, n_std):
        """Calculate ellipse parameters of the bivariate normal distribution
        Reference:
        - A geometric interpretation of the covariance matrix:
          https://www.visiondummy.com/2014/04/geometric-interpretation-covariance-matrix/
        - A proof that the contour of multivariate Normal distribution is an ellipsoid:
          https://stats.stackexchange.com/questions/326334/why-are-contours-of-a-multivariate-gaussian-distribution-elliptical
        """
        eigvals, eigvecs_ = np.linalg.eig(covariance)
        theta = np.arctan2(eigvecs_[1, :], eigvecs_[0, :])[0]
        ell_radius_x = n_std * np.sqrt(eigvals[0])  # or 'a', semi-major axis
        ell_radius_y = n_std * np.sqrt(eigvals[1])  # or 'b', semi-minor axis
        return np.asarray([theta, ell_radius_x, ell_radius_y])

    def _pdf(self, x, y):
        pos = np.dstack((x, y))
        # borrow scipy multivariate
        return multivariate_normal(self._mean[0], self._covariance).pdf(pos)

    def _cdf(self, x, y):
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        # borrow scipy multivariate
        return multivariate_normal(self._mean[0], self._covariance).cdf(np.asarray([x, y]))

    def _cdf_jointly_normal(self, x_lim, y_lim, *args):
        # if cross-correlation coefficient \rho is not zero, using integral of pdf is for convenience
        # todo: perform a check if cross-terms are zero
        f = integrate.nquad(lambda x, y: self._pdf(x, y), [[-np.inf, x_lim], [-np.inf, y_lim]])[0]
        return f

    def _pdf_jointly_normal(self, x, y):
        mu = self.mean
        sigma_1 = np.sqrt(self.covariance[0, 0])
        sigma_2 = np.sqrt(self.covariance[1, 1])
        rho = self.covariance[0, 1] / (sigma_1 * sigma_2)
        f = (
            1
            / (2 * np.pi * sigma_1 * sigma_2 * np.sqrt(1 - rho ** 2))
            * np.exp(
                -((x - mu[0]) ** 2) / (2 * (1 - rho ** 2) * sigma_1 ** 2)
                - (y - mu[1]) ** 2 / (2 * (1 - rho ** 2) * sigma_2 ** 2)
                + (rho * (x - mu[0]) * (y - mu[1])) / ((1 - rho ** 2) * sigma_1 * sigma_2)
            )
        )
        return f
