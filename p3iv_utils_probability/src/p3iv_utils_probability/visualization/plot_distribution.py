
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap
from util_probability.distributions import BivariateNormalDistribution, UnivariateNormalDistributionSequence  # , \

# TruncatedUnivariateNormalSequenceDistribution, UnivariateNormalSequenceMixtureDistribution, \
# TruncatedUnivariateNormalSequenceMixtureDistribution
rcParams["text.usetex"] = True


class PlotProbabilityDistribution(object):
    def __init__(self):
        self.colors = [
            "#FF0000",  # red
            "#800000",  # maroon
            "#0000FF",  # blue
            "#000080",  # navy
            "#008080",  # teal
            "#800080",  # purple
            "#9FE2BF",  # light-green
            "#FA8072",  # salmon
            "#CCCCFF",  # lila
            "#FF00FF",
        ]  # fuchsia

    def __call__(self, ax, distribution, *args, **kwargs):
        """Inspect the type of distribution and call the corresponding plot method."""
        assert isinstance(ax, plt.Axes)

        color = np.random.choice(self.colors)
        cmap = self.AlphaGradientColormap(color)

        if isinstance(distribution, BivariateNormalDistribution):
            self.plot_bivariate_pdf(ax, distribution, cmap=cmap)

        # elif isinstance(distribution, (UnivariateNormalSequenceDistribution, TruncatedUnivariateNormalSequenceDistribution)):
        elif isinstance(distribution, UnivariateNormalDistributionSequence):
            self.plot_univariate_sequence_cmap(ax, distribution, cmap=cmap)

            """
            elif isinstance(distribution, (UnivariateNormalSequenceMixtureDistribution, TruncatedUnivariateNormalSequenceMixtureDistribution)):
                self.plot_univariate_sequence_mixture(ax, distribution)
            """
        else:
            raise Exception("Plot function is not defined for data type %s" % str(type(distribution)))

    @staticmethod
    def AlphaGradientColormap(color):
        """
        Factory function for creating colormap instances with alpha gradient.
        :param color: Hex color code w/o alpha value e.g. '#AABBCC'
        :return: LinearSegmentedColormap instance
        """
        colors = [color + "00", color + "FF"]
        return LinearSegmentedColormap.from_list("alpha_gradient_color_map_" + color, colors)

    @staticmethod
    def plot_bivariate_pdf(ax, distribution, cmap="viridis", annotate=False):
        x, y = distribution.mean
        mesh_range = 10
        X, Y = np.meshgrid(
            np.linspace(x - mesh_range, x + mesh_range, 500), np.linspace(y - mesh_range, y + mesh_range, 500)
        )

        ax.contourf(X, Y, distribution.pdf(x, y, mesh_range=10), 50, cmap=cmap)

        if annotate:
            ax.annotate(
                r"$ \mu = (%.2f, %.2f) \\ "
                r"\Sigma = \left[\begin{array}{cc} %.2f & %.2f \\ %.2f & %.2f \\ \end{array}\right]$"
                % (
                    x,
                    y,
                    distribution.covariance[0, 0],
                    distribution.covariance[0, 1],
                    distribution.covariance[1, 0],
                    distribution.covariance[1, 1],
                ),
                (x, y - mesh_range + 2),
                textcoords="offset points",
                size=12,
            )

    def plot_bivariate_pdf_confidence_ellipse(self, ax, distribution, color=None, n_std=2):
        if not color:
            color = np.random.choice(self.colors)

        ax.plot(distribution.mean[0], distribution.mean[1], color=color, marker="o")
        for i in range(n_std):
            n = i + 1
            x, y, theta, ell_radius_x, ell_radius_y = distribution.range(n)
            ellipse = Ellipse(
                (0, 0),
                width=ell_radius_x * 2,
                height=ell_radius_y * 2,
                linestyle="dashed",
                edgecolor=color,
                facecolor="none",
                linewidth=1.5,
                label=r"$%d\sigma$" % n,
            )

            transf = transforms.Affine2D().rotate_deg(np.rad2deg(theta)).translate(x, y)

            ellipse.set_transform(transf + ax.transData)
            ax.add_patch(ellipse)

    def plot_bivariate_sequence_1d(self, ax, distribution, n_std=2):
        pass

    def plot_univariate_pdf(self, ax, distribution, n_std=3.0, weight=1.0):
        pass

    def plot_univariate_sequence(self, ax, distribution, color=None, n_std=3, weight=1.0):
        plots = []
        if not color:
            color = np.random.choice(self.colors)
        sequence_range = np.arange(len(distribution.mean))
        (p,) = ax.plot(sequence_range, distribution.mean, color=color, linestyle="--", linewidth=1)

        plots.append(p)

        gamma = 1 / n_std
        for i in range(n_std):
            n = i + 1
            lower_bound, upper_bound = distribution.range(n)
            c = ax.fill_between(sequence_range, upper_bound, lower_bound, facecolor=color, alpha=gamma * weight)
            plots.append(c)
        return plots

    @staticmethod
    def plot_univariate_sequence_cmap(ax, distribution, cmap="viridis", n_std=3, weight=1.0):
        max_std = np.max(distribution.covariance)

        # the points for which every distribution is calculated
        ny = 1000
        y0 = np.linspace(-n_std * max_std, n_std * max_std, ny)
        X, Y = np.meshgrid(list(range(len(distribution))), y0)
        Y += distribution.mean  # shift Y by the mean to get the true coordinates

        # map X and Y coordinates to indices of img
        Y = Y.astype(np.float)
        miny = np.min(Y)
        maxy = np.max(Y)
        y_idx = np.round((Y - miny) / (maxy - miny) * (ny - 1)).astype(np.int)

        X = X.astype(np.float)
        minx = np.min(X)
        maxx = np.max(X)
        nx = np.float(len(distribution))
        x_idx = np.round((X - minx) / (maxx - minx) * (nx - 1)).astype(np.int)

        # convert X, Y, Z to one array for imshow
        img = np.zeros((ny, len(distribution)))
        img[y_idx, x_idx] = distribution.pdf(Y, distribution.mean)

        extent = np.min(X), np.max(X), np.min(Y), np.max(Y)
        ax.imshow(img, cmap=cmap, origin="lower", aspect="auto", extent=extent)

    def plot_univariate_sequence_mixture(self, ax, tr_g_m, n_std=3):
        plots = []
        color = np.random.choice(self.colors)
        for i in range(len(tr_g_m.weights)):
            weight = tr_g_m.weights[i]
            tr_g = tr_g_m.components[i]
            pl = self.plot_univariate_sequence(ax, tr_g, color=color, n_std=n_std, weight=weight)
            plots.extend(pl)

        return plots
