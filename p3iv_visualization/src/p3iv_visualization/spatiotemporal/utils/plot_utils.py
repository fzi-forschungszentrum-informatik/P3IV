import matplotlib.pyplot as plt
import os


class PlotUtils(object):
    def __init__(self, fig=None, ax=None, header=None):
        self.fig = fig
        self.ax = ax
        self.header = header

        self.dt = None
        self.N = None
        self.output_dir = None

    def create_figure(self, header):
        self.header = header
        self.fig = plt.figure(header)
        self.fig.suptitle(header, fontsize=14, fontweight="bold")
        self.ax = plt.subplot(111)

    def set_settings(self, dt, N, output_dir):
        self.dt = dt
        self.N = N
        self.output_dir = output_dir

    def save_figure(self, w=24.0, h=15.0, file_format=".svg"):
        if os.path.isdir(self.output_dir) is False:
            os.makedirs(self.output_dir)
        self.fig.set_size_inches((w, h))
        self.fig.savefig(self.output_dir + self.header + file_format, dpi=self.fig.dpi)

    def set_labels(self, xlabel="Time $(s)$", ylabel="Longitudinal Position $(m)$"):
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def set_axis_limits(self, y_min, y_max):
        self.ax.set_xlim(0, self.N * self.dt)
        self.ax.set_ylim(y_min, y_max)
