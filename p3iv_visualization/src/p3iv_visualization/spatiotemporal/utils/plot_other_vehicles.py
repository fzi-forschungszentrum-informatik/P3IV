from util_probability.visualization.plot_truncated_gaussian_distribution import plot_distribution_confidence as p

# todo! Clear dep util_probability!


class PlotOtherVehicles(object):
    def __init__(self, ax, dt):
        self.ax = ax
        self.dt = dt
        self.ax_other_vehicles = []

    def plot_objects(self, combination, vehicle_colors):

        for i in range(len(combination.vehicles)):
            uncertain_motion = combination.vehicles[i]
            self.plot_object(uncertain_motion, vehicle_colors[i])

    def plot_object(self, uncertain_motion, color, weight=1.0, **kwargs):
        plots = p(self.ax, uncertain_motion, color, self.dt, weight=weight, **kwargs)
        self.ax_other_vehicles.extend(plots)

    def clear_objects(self):
        if self.ax:
            for i in self.ax_other_vehicles:
                try:
                    i.remove()
                except ValueError:
                    # ValueError: list.remove(x): x not in list
                    pass
