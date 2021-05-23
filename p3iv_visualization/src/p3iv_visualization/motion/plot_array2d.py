import numpy as np


class PlotArray2D(object):
    def __init__(self, ax, y_label, x_label="Time $(s)$", label_lon="Longitudinal motion", label_lat="Lateral motion"):
        self.ax = ax
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)

        self.color_x = "#2c7fb8"
        self.color_y = "#31a354"
        self.color_m = "#756bb1"

        self.t = None
        # Set up the elements we want to animate
        # <lineobject>.set_data() does not support packing 2D arrays as y value
        # Therefore, we define separate line objects for each component
        (self.ax_x_pinn,) = self.ax.plot([], [], "o-", label=label_lon, color=self.color_x)
        (self.ax_x_free,) = self.ax.plot([], [], "o-", color=self.color_x, alpha=0.25)
        (self.ax_y_pinn,) = self.ax.plot([], [], "o-", label=label_lat, color=self.color_y)
        (self.ax_y_free,) = self.ax.plot([], [], "o-", color=self.color_y, alpha=0.25)
        (self.ax_m_pinn,) = self.ax.plot([], [], "o-", color=self.color_m)
        (self.ax_m_free,) = self.ax.plot([], [], "o-", color=self.color_m, alpha=0.25)

    def initialize(self, timesteps):
        self.t = timesteps

    def update_motion_array2d(self, motion_array2d, index4pin2free=0, magnitude_flag=True):

        if index4pin2free > 0:
            data_pinn = motion_array2d[:index4pin2free]
            data_free = motion_array2d[index4pin2free - 1 :]

            self.ax_x_pinn.set_data(self.t[:index4pin2free], data_pinn[:, 0])
            self.ax_y_pinn.set_data(self.t[:index4pin2free], data_pinn[:, 1])
            self.ax_x_free.set_data(self.t[index4pin2free - 1 :], data_free[:, 0])
            self.ax_y_free.set_data(self.t[index4pin2free - 1 :], data_free[:, 1])

        else:
            data_pinn = motion_array2d
            self.ax_x_pinn.set_data(self.t, data_pinn[:, 0])
            self.ax_y_pinn.set_data(self.t, data_pinn[:, 1])

        if magnitude_flag:
            magnitude = np.linalg.norm(motion_array2d, axis=1)
            if index4pin2free > 0:
                self.ax_m_pinn.set_data(self.t[:index4pin2free], magnitude[:index4pin2free])
                self.ax_m_free.set_data(self.t[index4pin2free - 1 :], magnitude[index4pin2free - 1 :])
            else:
                self.ax_m_pinn.set_data(self.t, magnitude)

        else:
            # the last magnitude line remains on the plot, if this block is deleted!
            self.ax_m_free.set_data([], [])
            self.ax_m_pinn.set_data([], [])

    def set_x_axis(self, increment=2, set_ticks=True):
        """
        Define axis limits and ticks
        increment   : increment in x-ticks
        """
        t_final = self.t[-1]
        ticks = [int(i) for i in np.arange(0, t_final + 1, increment)]

        self.ax.set_xlim(0, t_final)
        self.ax.set_xticks(ticks)

        if set_ticks:
            tick_labels = map(str, ticks)
        else:
            tick_labels = ""
        self.ax.set_xticklabels(tick_labels)

    def set_y_axis(self, y_min, y_max, increment=2):
        """
        Define axis limits and ticks
        increment   : increment in y-ticks
        """
        lim_min = (y_min / increment) * increment  # round out the min_val to an upper increment
        lim_max = np.ceil(y_max / increment) * increment  # round out the max_val to an upper increment
        self.ax.set_ylim(lim_min, lim_max)
        self.ax.set_yticks(np.arange(lim_min, lim_max, increment))


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1)
    p = PlotArray2D(ax, "Timesteps")

    timesteps_ = np.arange(12) * 0.5
    p.initialize(timesteps_)
    p.set_x_axis()
    p.set_y_axis(-2, 20, increment=3)

    motion_array2d = np.zeros(24).reshape(-1, 2)
    motion_array2d[:, 0] = 5 * np.ones(12) + np.arange(12)
    motion_array2d[:, 1] = 4 * np.ones(12)
    p.update_motion_array2d(motion_array2d, index4pin2free=5)

    plt.show()
