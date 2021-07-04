import numpy as np
from p3iv_utils_probability.distributions import UnivariateNormalDistributionSequence
from p3iv_utils_probability.visualization.plot_truncated_gaussian_distribution import plot_distribution_confidence as p


class PlotOtherVehicles(object):
    def __init__(self, ax, dt):
        self.ax = ax
        self.dt = dt
        self.ax_other_vehicles = []

    def plot_object(self, motion_array, progress_array, overlap, color, weight=1.0, **kwargs):
        time_range = np.arange(len(progress_array)) * self.dt
        time_range = time_range[overlap]

        d = UnivariateNormalDistributionSequence()
        d.resize(len(time_range))
        d.mean = progress_array[:, 0][overlap]
        # todo@sahin: replace this line with the one below
        d.covariance = np.ones(len(d.mean)) * 2.0
        # d.covariance = self.get_longitudinal_covariance(motion_array, progress_array)
        plots = p(self.ax, d, time_range, color, self.dt, weight=weight, **kwargs)
        self.ax_other_vehicles.extend(plots)

    def clear_objects(self):
        if self.ax:
            for i in self.ax_other_vehicles:
                try:
                    i.remove()
                except ValueError:
                    # ValueError: list.remove(x): x not in list
                    pass

    @staticmethod
    def get_longitudinal_covariance(motion_array, progress_array):
        covariance = np.empty(len(progress_array))
        for i in range(len(motion_array.position)):
            covariance[i] = motion_array.position.covariance[i][0, 0]
        return covariance
