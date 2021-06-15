import numpy as np


class PlotArray2D(object):
    def __init__(self, ax, y_label, x_label="Time $(s)$", label_x="x-component", label_y="y-component"):
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
        (self.ax_x_pinn,) = self.ax.plot([], [], "o-", label=label_x, color=self.color_x)
        (self.ax_x_free,) = self.ax.plot([], [], "o-", color=self.color_x, alpha=0.25)
        (self.ax_y_pinn,) = self.ax.plot([], [], "o-", label=label_y, color=self.color_y)
        (self.ax_y_free,) = self.ax.plot([], [], "o-", color=self.color_y, alpha=0.25)
        (self.ax_m_pinn,) = self.ax.plot([], [], "o-", color=self.color_m)
        (self.ax_m_free,) = self.ax.plot([], [], "o-", color=self.color_m, alpha=0.25)

    def initialize(self, timesteps):
        self.t = timesteps

    def update_motion_array1d(self, motion_array1d, index4pin2free=0, magnitude_flag=True):

        self._update_motion_array(self.ax_m_pinn, self.ax_m_free, motion_array1d, index4pin2free=index4pin2free)

    def update_motion_array2d(self, motion_array2d, index4pin2free=0, magnitude_flag=True):

        self._update_motion_array(self.ax_x_pinn, self.ax_x_free, motion_array2d[:, 0], index4pin2free=index4pin2free)
        self._update_motion_array(self.ax_y_pinn, self.ax_y_free, motion_array2d[:, 1], index4pin2free=index4pin2free)
        self._update_magnitude_array(motion_array2d, index4pin2free, magnitude_flag)

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
            tick_labels = list(map(str, ticks))
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

    def _update_motion_array(self, ax_pinn, ax_free, data, index4pin2free):

        if index4pin2free > 0:
            data_pinn = data[:index4pin2free]
            data_free = data[index4pin2free - 1 :]

            ax_pinn.set_data(self.t[:index4pin2free], data_pinn)
            ax_free.set_data(self.t[index4pin2free - 1 :], data_free)

        else:
            # data_pinn is equal to data
            ax_pinn.set_data(self.t, data)

    def _update_magnitude_array(self, data, index4pin2free, magnitude_flag):
        if magnitude_flag:
            magnitude = np.linalg.norm(data, axis=1)
            if index4pin2free > 0:
                self.ax_m_pinn.set_data(self.t[:index4pin2free], magnitude[:index4pin2free])
                self.ax_m_free.set_data(self.t[index4pin2free - 1 :], magnitude[index4pin2free - 1 :])
            else:
                self.ax_m_pinn.set_data(self.t, magnitude)

        else:
            # the last magnitude line remains on the plot, if this block is deleted!
            self.ax_m_free.set_data([], [])
            self.ax_m_pinn.set_data([], [])
