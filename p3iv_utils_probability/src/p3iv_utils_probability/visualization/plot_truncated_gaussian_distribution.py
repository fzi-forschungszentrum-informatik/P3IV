import numpy as np
from p3iv_utils_probability.distributions import UnivariateNormalDistribution, BivariateNormalDistributionSequence
from p3iv_utils_probability.distributions import UnivariateNormalDistributionSequence


def plot_univariate_normal_distribution(ax, tr_g, color, dt, weight=1.0, sigma=3):

    plots = []

    time_range = np.arange(len(tr_g.mean)) * dt
    (p,) = ax.plot(time_range, tr_g.mean, color=color, linestyle="--", linewidth=1)

    plots.append(p)

    gamma = 1 / sigma
    for i in range(1, sigma + 1):
        range_array = tr_g.range(i)
        lower_bound = range_array[:, 0]
        upper_bound = range_array[:, 1]
        c = ax.fill_between(time_range, upper_bound, lower_bound, facecolor=color, alpha=gamma * weight)
        plots.append(c)
    return plots


def plot_bivariate_normal_distribution_1d(ax, tr_g, color, dt, weight=1.0, sigma=3, offset=0.0):
    """

    Parameters
    ----------
    tr_g: BivariateNormalDistributionSequence
        Distribution to plot.
    offset: double
        Offset to subtract from y-axis values.
    """

    plots = []

    time_range = np.arange(len(tr_g.mean)) * dt

    l = len(tr_g.mean)
    covariance = np.zeros([l, 2, 2])
    v00 = np.ones(l) * 2.0
    v11 = np.ones(l) * 2.0
    covariance[:, 0, 0] = v00
    covariance[:, 1, 1] = v11
    tr_g.covariance = covariance

    # plot the mean with dashed lines
    mean = tr_g.mean[:, 0]
    (p,) = ax.plot(time_range, mean - offset, color=color, linestyle="--", linewidth=1)
    plots.append(p)

    gamma = 1 / sigma
    for i in range(1, sigma + 1):
        # use ellipse radius-x for calculations
        pseudo_sigma = tr_g.upper_bound(i)[:, 3]
        mean = tr_g.upper_bound(i)[:, 0]

        upper_bound = mean + pseudo_sigma - offset
        lower_bound = mean - pseudo_sigma - offset

        c = ax.fill_between(time_range, upper_bound, lower_bound, facecolor=color, alpha=gamma * weight)
        plots.append(c)
    return plots


def plot_truncated_gaussian_mixture_distribution_confidence(ax, tr_g_m, color, dt, sigma=3):

    plots = []
    for i in range(len(tr_g_m.weights)):
        weight = tr_g_m.weights[i]
        tr_g = tr_g_m.components[i]
        pl = plot_truncated_gaussian_distribution_confidence(ax, tr_g, color, dt, weight=weight, sigma=sigma)
        plots.extend(pl)

    return plots


def plot_distribution_confidence(ax, data, color, dt, sigma=3, weight=1.0, **kwargs):
    if isinstance(data, UnivariateNormalDistribution):
        return plot_univariate_normal_distribution(ax, data, color, dt, weight=weight, sigma=sigma)
    if isinstance(data, BivariateNormalDistributionSequence):
        return plot_bivariate_normal_distribution_1d(ax, data, color, dt, weight=weight, sigma=sigma, **kwargs)
    elif isinstance(data, UnivariateNormalDistributionSequence):
        return plot_truncated_gaussian_mixture_distribution_confidence(ax, data, color, dt, sigma=sigma, **kwargs)
    else:
        print(type(data))
        raise Exception("Plot function is not defined for this data type")
