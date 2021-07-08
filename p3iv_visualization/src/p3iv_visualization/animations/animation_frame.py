import os
from functools import partial
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider, Button


class AnimationFrame(object):
    def __init__(self):
        self.header = "P3IV Simulator"

        self.step = 0  # frame step number
        self.pause_flag = False

        self.save_figure_flag = True
        self.zoom = 30

        self.fig = None
        self.ax0 = None
        self.ax1 = None
        self.ax2 = None
        self.ax3 = None
        self.ax4 = None

        self.pause_button = None
        self.previous_button = None
        self.next_button = None
        self.zoom_slider = None

    def create_subplots(self):
        self.fig = plt.figure(self.header, figsize=(21, 7), dpi=100)
        # A 15.6" 16x9 screen is 13.60" wide, 7.65" high and a res. of 1366x768 for 15.6" corresponds to 100dpi
        self.fig.suptitle(self.header, fontsize=14, fontweight="bold")

        # specify the geometry of the grid that the subplots will be placed
        gs = gridspec.GridSpec(3, 3)

        # Define the a rectangle for the both subplots in axes coordinates
        # l, r, b, h stand for left, right, bottom, figure height respectively
        l = 0.03
        r = 1 - l
        b, h = 0.12, 0.75
        # 'ws' stands for the amount of width reserved for blank space between subplots
        ws = 0.20

        # Update the GridSpace according to the box defined above
        gs.update(left=l, bottom=b, right=r, top=b + h, wspace=ws, hspace=0.00)

        self.ax0 = plt.subplot(gs[:, 0])
        self.ax1 = plt.subplot(gs[:, 1])
        self.ax2 = plt.subplot(gs[0, 2])
        self.ax3 = plt.subplot(gs[1, 2])
        self.ax4 = plt.subplot(gs[2, 2])

    def set_rc_params(self):
        # set the font etc. of required items
        # matplotlib > 1.4.x
        params = {
            "legend.fontsize": 8,
            "font.size": 19,
            "xtick.major.size": 20,  # !
            "xtick.minor.size": 8,  # !
            "lines.linewidth": 1,
            "lines.markersize": 4,
            "animation.frame_format": "png",
        }
        plt.rcParams.update(params)

    def set_header(self, header):
        self.header = str(header)

    def set_subplot_titles(self):
        # location parameters 0.5 and 1.09 are tuned per trial&error
        self.ax0.text(
            0.5,
            1.05,
            "Path-Time Diagram",
            horizontalalignment="center",
            verticalalignment="bottom",
            transform=self.ax0.transAxes,
            fontsize=12,
        )

        self.ax1.text(
            0.5,
            1.05,
            "Cartesian Mapping of Motion",
            horizontalalignment="center",
            verticalalignment="bottom",
            transform=self.ax1.transAxes,
            fontsize=12,
        )

        self.ax2.text(
            0.5,
            1.16,
            "Velocity, Speed and Control Inputs",
            horizontalalignment="center",
            verticalalignment="bottom",
            transform=self.ax2.transAxes,
            fontsize=12,
        )

    @staticmethod
    def button_defaults(button_set_function):
        # Define a button for the pause event
        button_height = 0.03
        button_level = 0.02
        button_width = 0.07
        x_button = 0.71
        delta_button = 0.08
        return partial(
            button_set_function,
            button_height=button_height,
            button_level=button_level,
            button_width=button_width,
            x_button=x_button,
            delta_button=delta_button,
        )

    def __set_previous_box(self, x_button, button_level, button_width, button_height, delta_button, **kwargs):
        # Define a button in order to save the current instance as svg#
        previous_box = plt.axes([x_button + delta_button, button_level, button_width, button_height])
        self.previous_button = Button(previous_box, "Previous frame", hovercolor="0.975")

    def __set_pause_box(self, x_button, button_level, button_width, button_height, **kwargs):
        pause_box = plt.axes([x_button, button_level, button_width, button_height])

        if not self.pause_flag:
            self.pause_button = Button(pause_box, "Pause", hovercolor="0.975")
        else:
            self.pause_button = Button(pause_box, "Resume", hovercolor="0.975")

    def __set_next_box(self, x_button, button_level, button_width, button_height, delta_button, **kwargs):
        # Define a button in order to display the magnitude of x- and y-components
        next_box = plt.axes([x_button + 2 * delta_button, button_level, button_width, button_height])
        self.next_button = Button(next_box, "Next frame", hovercolor="0.975")

    def set_buttons(self):
        self.button_defaults(self.__set_previous_box)()
        self.button_defaults(self.__set_pause_box)()
        self.button_defaults(self.__set_next_box)()
        self.button_defaults(self.__set_zoom_slider)()

        # set callbacks
        self.pause_button.on_clicked(self.__pause_action)
        self.previous_button.on_clicked(self.__previous_action)
        self.next_button.on_clicked(self.__next_action)
        self.zoom_slider.on_changed(self.__slider_update)

    def __previous_action(self, event):
        """
        Set up an event callback to decrement frame number.
        """
        self.step -= 1

    def __pause_action(self, event):
        """
        Set up an event callback for a pause button.
        """
        self.pause_flag ^= True
        # if paused, change the label of the button widget with 'Resume'
        if self.pause_flag is True:
            self.pause_button.label.set_text("Resume")
        # once resumed, change the label back to 'Pause'. Not 'elif', because pause could be initialized as 'True'.
        if self.pause_flag is not True:
            self.pause_button.label.set_text("Pause")
        print("\nAnimation paused\n")

    def __next_action(self, event):
        """
        Set up an event callback to increment frame number.
        """
        self.step += 1

    def __set_zoom_slider(self, button_level, button_height, **kwargs):
        # Define the position of the slider as a box in axes coordinates [left, bottom, width, height]
        zoom_bar_height = 0.01
        zoom_box = plt.axes([0.38, button_level + (button_height - zoom_bar_height) / 2, 0.23, zoom_bar_height])

        # Define the slider
        zoom_val_min, zoom_val_max = 10, 200
        self.zoom_slider = Slider(zoom_box, "Zoom", zoom_val_min, zoom_val_max, valinit=self.zoom)

    def __slider_update(self, val):
        self.zoom = self.zoom_slider.val

    def save_animation_instance(self, save_dir, i_anim):
        if self.save_figure_flag:
            save_file_name = "step_{:03}.png".format(i_anim)
            save_file_dir = os.path.join(save_dir, save_file_name)
            print(("The figure is being saved to:\n" + str(save_file_dir)))
            self.fig.savefig(save_file_dir, format="png", dpi=self.fig.dpi)


if __name__ == "__main__":
    animate_single = AnimationFrame()
    animate_single.create_subplots()
    # animate_single.set_rc_params()
    animate_single.set_subplot_titles()
    animate_single.set_buttons()
    # animate_single.fig.show()
    plt.show()
