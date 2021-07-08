import numpy as np
from p3iv_visualization.motion.plot_array2d import PlotArray2D


class PlotMotionComponents(object):
    def __init__(
        self,
        ax0,
        ax1,
        ax2,
        ax0_label="Velocity $(m/s)$",
        ax1_label="Speed $(m/s)$",
        ax2_label="Control Inputs",
    ):
        self.p_ax0 = PlotArray2D(ax0, y_label=ax0_label, label_x="x-component", label_y="y-component")
        self.p_ax1 = PlotArray2D(ax1, y_label=ax1_label)
        self.p_ax2 = PlotArray2D(
            ax2, y_label=ax2_label, label_x="Steering angle $(deg)$", label_y="Acceleration $(m/s^2)$"
        )

        self.lines_axvline_0 = ax0.axvline(x=-1, linewidth=0.5, color="r")
        self.lines_axvline_1 = ax1.axvline(x=-1, linewidth=0.5, color="r")
        self.lines_axvline_2 = ax2.axvline(x=-1, linewidth=0.5, color="r")

        ax2_twin = ax2.twinx()
        self.p_ax2_twin = PlotArray2D(ax2_twin)

    def initialize(self, timesteps):
        self.p_ax0.initialize(timesteps)
        self.p_ax0.set_x_axis(set_ticks=False)
        self.p_ax0.set_y_axis(-20, 20, increment=5)

        self.p_ax1.initialize(timesteps)
        self.p_ax1.set_x_axis(set_ticks=False)
        self.p_ax1.set_y_axis(0, 20, increment=3)

        self.p_ax2.initialize(timesteps)
        self.p_ax2.set_x_axis()
        self.p_ax2.set_y_axis(-90, 90, increment=30)

        self.p_ax2_twin.initialize(timesteps)
        self.p_ax2_twin.set_x_axis()
        self.p_ax2_twin.set_y_axis(-10, 10, increment=5)

        # hide the x-labels of the 2nd and the 3rd subplot
        # but this is not necessary: set_ticks is False in ax.set_x_axis(set_ticks=False)
        # plt.setp(ax0.get_xticklabels() + ax1.get_xticklabels(), visible=False)

    def update_profile(self, ax0_data=None, ax1_data=None, ax2_data=None, index4pin2free=0, magnitude_flag=False):
        """
        Parameters
        -----------
        :param motion_profile: an object representing motion profile of type Motion
        :param index4pin2free: index value to switch from opaque to transparent
        :param magnitude_flag: show magnitude line as well (boolean)
        :return:
        """
        if ax0_data is not None:
            for ax, data in zip([self.p_ax0, self.p_ax1], [ax0_data, ax1_data]):

                if len(data.shape) == 1:
                    ax.update_motion_array1d(data, index4pin2free=index4pin2free, magnitude_flag=magnitude_flag)
                else:
                    ax.update_motion_array2d(data, index4pin2free=index4pin2free, magnitude_flag=magnitude_flag)

            # not elegant due to twin plot; but modify lowest row manually
            self.p_ax2._update_motion_array(
                self.p_ax2.ax_x_pinn, self.p_ax2.ax_x_free, ax2_data[:, 0], index4pin2free=index4pin2free
            )
            self.p_ax2._update_motion_array(
                self.p_ax2_twin.ax_y_pinn, self.p_ax2_twin.ax_y_free, ax2_data[:, 1], index4pin2free=index4pin2free
            )

    def update_time_highlighter(self, t):
        self.lines_axvline_0.set_xdata(t)
        self.lines_axvline_1.set_xdata(t)
        self.lines_axvline_2.set_xdata(t)

    def set_labels(self):
        # Define a legend in order to specify the x-y components of the plotted item
        # (numpoints is for setting the number of markers shown in the legend )
        self.p_ax0.ax.legend(
            bbox_to_anchor=(0.005, 0.88, 0.99, 0.10),
            loc="center",
            ncol=2,
            mode="expand",
            borderaxespad=0.0,
            numpoints=1,
            prop={"size": 8},
        )

        self.p_ax2.ax.legend(
            bbox_to_anchor=(0.005, 0.87, 0.99, 0.10),
            loc="center",
            ncol=2,
            mode="expand",
            borderaxespad=0.0,
            numpoints=1,
            prop={"size": 8},
        )

    def add_pickable_area(self):
        # todo: not implemented yet. is just a 'nice to have'
        """
        # Get the x and y-lines objects
        l1=self.p_ax0.ax.legend(bbox_to_anchor=(0, 1, 1, 0.100), loc=3, ncol=2, mode="expand", borderaxespad=0., numpoints=1)
        l1x, l1y = self.l1.get_lines()

        # Define the area of the picker
        l1x.set_picker(60)
        l1y.set_picker(60)

        # Define a second legend for magnitude, to upper right corner
        self.l2 = self.ax2.legend([self.ax2_vel_m], ["Magnitude"], loc='upper right', fancybox=True)
        # Increase the transparency so that the lines behind can be seen
        self.l2.get_frame().set_alpha(0.4)
        # Defining a second label removes l1 from the axes.
        # Therefore, l1 must be added as a separate artist to the axes
        self.ax2.add_artist(self.l1)
        # plt.legend((line1, line2), ('label1', 'label2'), 'upper right')
        """
        pass
