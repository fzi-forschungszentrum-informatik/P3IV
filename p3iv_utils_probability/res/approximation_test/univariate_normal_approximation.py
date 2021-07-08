# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from util_probability.distributions import UnivariateNormalDistribution, BivariateNormalDistribution


def plot_univariate_normal(ax, UnivariateNormalDistribution, x, label=None, scaling_factor=1):
    # x = get_x_range(UnivariateNormalDistribution, n_std=n_std)
    ax.plot(x, scaling_factor * UnivariateNormalDistribution.pdf(x), label=label)


def get_x_range(uvn, n_std=4):
    center = uvn.mean.flatten()[0]
    deviation = np.sqrt(uvn.covariance.flatten()[0])
    x = np.linspace(center - n_std * deviation, center + n_std * deviation, 500)
    return x


def uvn_product(uvn1, uvn2):
    assert isinstance(uvn1, UnivariateNormalDistribution)
    assert isinstance(uvn2, UnivariateNormalDistribution)
    s, mu_12, sigma_12 = _cal_par(uvn1.mean[0], np.sqrt(uvn1.covariance[0]), uvn2.mean[0], np.sqrt(uvn2.covariance[0]))
    return s, UnivariateNormalDistribution(mean=mu_12, covariance=sigma_12)


def _cal_par(mu1, sigma1, mu2, sigma2):
    mu_12 = (mu1 * sigma2 ** 2 + mu2 * sigma1 ** 2) / (sigma1 ** 2 + sigma2 ** 2)
    sigma_12 = np.sqrt((sigma1 ** 2 * sigma2 ** 2) / (sigma1 ** 2 + sigma2 ** 2))
    s = (
        1
        / (np.sqrt(2 * np.pi * (sigma1 ** 2 + sigma2 ** 2)))
        * np.exp(-((mu1 - mu2) ** 2 / (2 * (sigma1 ** 2 + sigma2 ** 2))))
    )
    return s, mu_12, sigma_12


def cal_uncertainty_of_mul(mu1, cov1, mu2, cov2):
    return mu2 ** 2 * cov1 + mu1 ** 2 * cov2


def get_diff_integral_list(uvn1, uvn2, n_std=4):
    abs_diff = lambda a: np.abs(uvn1.pdf(a) - uvn2.pdf(a))
    span = get_x_range(uvn1, n_std=n_std)
    result = []
    for val in span:
        result.append(integrate.quad(abs_diff, span[0], val)[0])
    return result


def get_diff_integral(uvn1, uvn2, n_std=4):
    abs_diff = lambda a: np.abs(uvn1.pdf(a) - uvn2.pdf(a))
    lower_lim = min(uvn1.mean[0] - n_std * uvn1.covariance[0], uvn1.mean[0] - n_std * uvn1.covariance[0])
    x_upper_lim = -lower_lim
    result = integrate.quad(abs_diff, lower_lim, x_upper_lim)[0]
    return result


def error_vs_sigma_mu_ratio(mean_1, cov_1, mean_2, cov_2, n_std=5):
    uvn_1 = UnivariateNormalDistribution(mean=mean_1, covariance=cov_1)
    uvn_2 = UnivariateNormalDistribution(mean=mean_2, covariance=cov_2)

    s, uvn_12 = uvn_product(uvn_1, uvn_2)
    mean_uncertainty = mean_1 * mean_2
    cov_uncertainty = cal_uncertainty_of_mul(mean_1, cov_1, mean_2, cov_2)
    uvn_12_uncertainty = UnivariateNormalDistribution(mean=mean_uncertainty, covariance=cov_uncertainty)

    ratio_12 = uvn_12.covariance[0] / uvn_12.mean[0]
    ratio_uncertainty_12 = uvn_12_uncertainty.covariance[0] / uvn_12_uncertainty.mean[0]

    diff_integ = get_diff_integral(uvn_1, uvn_2, n_std=n_std)

    return ratio_12, ratio_uncertainty_12, diff_integ


if __name__ == "__main__":
    error_vs_sigma_mu_ratio(1.0, 5.0, 2.0, 3.0)
    m_1 = 1.0
    v_1 = 5.0
    uvn_1 = UnivariateNormalDistribution(mean=m_1, covariance=v_1)

    m_2 = 2.0
    v_2 = 3.0
    uvn_2 = UnivariateNormalDistribution(mean=m_2, covariance=v_2)

    s, uvn_12 = uvn_product(uvn_1, uvn_2)
    print("The mean and the covariance of the pdf product calculated from equations are:")
    print((uvn_12.mean[0], uvn_12.covariance[0]))
    print("-------")

    mean_uncertainty = m_1 * m_2
    cov_uncertainty = cal_uncertainty_of_mul(m_1, v_1, m_2, v_2)
    uvn_12_uncertainty = UnivariateNormalDistribution(mean=mean_uncertainty, covariance=cov_uncertainty)
    print("The mean and the covariance of the pdf product calculated from propagation of uncertainty are:")
    print((uvn_12_uncertainty.mean[0], uvn_12_uncertainty.covariance[0]))
    print("-------")

    fig = plt.figure()
    ax0 = fig.add_subplot(111)
    x_range = 5
    x = get_x_range(uvn_12_uncertainty, n_std=x_range)

    # plot_univariate_normal(ax0, uvn_1, n_std=x_range)
    # plot_univariate_normal(ax0, uvn_2, n_std=x_range)
    plot_univariate_normal(ax0, uvn_12, x, label="by equations", scaling_factor=1)
    plot_univariate_normal(ax0, uvn_12_uncertainty, x, label="by propagation of uncertainty")

    ax0.plot(x, np.abs(uvn_12.pdf(x) - uvn_12_uncertainty.pdf(x)), "--", label="absolute difference")

    # diff_integ_list = get_diff_integral_list(uvn_12, uvn_12_uncertainty, n_std=x_range)
    # ax0.plot(x, diff_integ_list, 'b-')

    print((get_diff_integral(uvn_12, uvn_12_uncertainty, n_std=x_range)))

    # print(integrate.quad(lambda a: uvn_12_uncertainty.pdf(a), -np.inf, np.inf)[0])
    # print(integrate.quad(lambda a: uvn_12.pdf(a), -np.inf, np.inf)[0])
    r_12, r_u_12, diff_integ = error_vs_sigma_mu_ratio(1, 5, 2, 3)
    print((r_12, r_u_12, diff_integ))

    ax0.legend()
    plt.show()
