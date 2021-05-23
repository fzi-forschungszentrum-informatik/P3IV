import numpy as np
from p3iv_visualization.motion.plot_array2d import PlotArray2D


class PlotMotionComponents(object):
    def __init__(
        self,
        ax0,
        ax1,
        ax2,
        ax0_label="Velocity $(m/s)$",
        ax1_label="Acceleration $(m/s^2)$",
        ax2_label="Jerk $(m/s^3)$",
    ):
        self.p_ax0 = PlotArray2D(ax0, y_label=ax0_label)
        self.p_ax1 = PlotArray2D(ax1, y_label=ax1_label)
        self.p_ax2 = PlotArray2D(ax2, y_label=ax2_label)

        self.lines_axvline_0 = ax0.axvline(x=-1, linewidth=0.5, color="r")
        self.lines_axvline_1 = ax1.axvline(x=-1, linewidth=0.5, color="r")
        self.lines_axvline_2 = ax2.axvline(x=-1, linewidth=0.5, color="r")

    def initialize(self, timesteps):
        self.p_ax0.initialize(timesteps)
        self.p_ax0.set_x_axis(set_ticks=False)
        self.p_ax0.set_y_axis(-2, 20, increment=3)

        self.p_ax1.initialize(timesteps)
        self.p_ax1.set_x_axis(set_ticks=False)
        self.p_ax1.set_y_axis(-2, 20, increment=3)

        self.p_ax2.initialize(timesteps)
        self.p_ax2.set_x_axis()
        self.p_ax2.set_y_axis(-2, 20, increment=3)

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
        for ax, data in zip([self.p_ax0, self.p_ax1, self.p_ax2], [ax0_data, ax1_data, ax2_data]):
            if data is not None:
                ax.update_motion_array2d(data, index4pin2free=index4pin2free, magnitude_flag=magnitude_flag)

    def update_time_highlighter(self, t):
        self.lines_axvline_0.set_xdata(t)
        self.lines_axvline_1.set_xdata(t)
        self.lines_axvline_2.set_xdata(t)

    def set_labels(self):
        # Define a legend in order to specify the x-y components of the plotted item
        # (numpoints is for setting the number of markers shown in the legend )
        self.p_ax0.ax.legend(
            bbox_to_anchor=(0, 1, 1, 0.100), loc=3, ncol=2, mode="expand", borderaxespad=0.0, numpoints=1
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


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from util_motion.motion_sequence import MotionSequence

    m_frenet = MotionSequence()
    m_frenet.position = np.array(
        [
            [4.92560704e01, 1.41206491e-15],
            [5.00560704e01, -1.81126815e-15],
            [5.08560704e01, 2.98372438e-16],
            [5.17232704e01, -1.14838694e-15],
            [5.27024704e01, 2.06952511e-15],
            [5.37936704e01, -1.87350135e-15],
            [5.49999075e01, -1.08940634e-15],
            [5.63190916e01, 2.49800181e-15],
            [5.77454961e01, -1.29236899e-15],
            [5.92709730e01, -2.76861867e-15],
            [6.08859243e01, -4.51881314e-16],
            [6.25800593e01, -4.71844785e-16],
            [6.43429694e01, -4.57966998e-16],
            [6.61645485e01, 8.67361738e-16],
        ]
    )

    m_frenet.velocity = np.array(
        [
            [0.00000000e00, 0.00000000e00],
            [4.00000000e00, -1.61166653e-14],
            [4.00000000e00, 1.05482029e-14],
            [4.33600000e00, -7.23379689e-15],
            [4.89600000e00, 1.60895602e-14],
            [5.45600000e00, -1.97151323e-14],
            [6.03118564e00, 3.92047506e-15],
            [6.59592080e00, 1.79370407e-14],
            [7.13202224e00, -1.89518540e-14],
            [7.62738442e00, -7.38124839e-15],
            [8.07475648e00, 1.15836868e-14],
            [8.47067513e00, -9.98173551e-17],
            [8.81455030e00, 6.93889390e-17],
            [9.10789555e00, 6.62664368e-15],
        ]
    )

    m_frenet.acceleration = np.array(
        [
            [0.00000000e00, 0.00000000e00],
            [0.00000000e00, 0.00000000e00],
            [-1.77635684e-13, 1.33324341e-13],
            [1.68000000e00, -8.89099992e-14],
            [2.80000000e00, 1.16616786e-13],
            [2.80000000e00, -1.79023463e-13],
            [2.87592818e00, 1.18178037e-13],
            [2.82367581e00, 7.00828284e-14],
            [2.68050723e00, -1.84444474e-13],
            [2.47681090e00, 5.78530279e-14],
            [2.23686028e00, 9.48246758e-14],
            [1.97959324e00, -5.84175206e-14],
            [1.71937588e00, 8.46031470e-16],
            [1.46672621e00, 3.27862737e-14],
        ]
    )

    m_frenet.jerk = np.array(
        [
            [0.00000000e00, 0.00000000e00],
            [0.00000000e00, 0.00000000e00],
            [0.00000000e00, 0.00000000e00],
            [8.40000000e00, -1.11117170e-12],
            [5.60000000e00, 1.02763392e-12],
            [-9.76996262e-12, -1.47820124e-12],
            [3.79640891e-01, 1.48600750e-12],
            [-2.61261842e-01, -2.40476042e-13],
            [-7.15842895e-01, -1.27263651e-12],
            [-1.01848163e00, 1.21148751e-12],
            [-1.19975314e00, 1.84858239e-13],
            [-1.28633516e00, -7.66210982e-13],
            [-1.30108684e00, 2.96317760e-13],
            [-1.26324832e00, 1.59701211e-13],
        ]
    )

    timesteps_ = np.arange(len(m_frenet)) * 0.5

    fig = plt.figure(1)

    gs = gridspec.GridSpec(3, 1)
    gs.update(hspace=0.00)
    ax0 = plt.subplot(gs[0, 0])
    ax1 = plt.subplot(gs[1, 0])
    ax2 = plt.subplot(gs[2, 0])

    p = PlotMotionSequence(ax0, ax1, ax2)
    p.initialize(timesteps_)
    p.set_labels()
    p.update_profile(m_frenet, index4pin2free=6)

    plt.show()
