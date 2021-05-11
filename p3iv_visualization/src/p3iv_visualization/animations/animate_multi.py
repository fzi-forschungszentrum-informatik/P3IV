from __future__ import division
from animator import Animator
import os
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class AnimateMulti(object):
    def __init__(self, ground_truth, configurations):

        map_image_name = configurations["map"]
        imagery_data = None
        self.egovehicle = ground_truth[configurations["vehicle_of_interest"]]

        self.n = configurations["temporal"]["N"]
        self.dt = configurations["temporal"]["dt"] / 1000
        n_pin_past = configurations["temporal"]["N_pin_past"]
        n_pin_future = configurations["temporal"]["N_pin_future"]
        self.save_dir = configurations["save_dir"]

        map_filename = configurations["map"] + ".osm"
        lanelet_map_file = os.path.abspath(
            os.path.join(configurations["save_dir"], configurations["interaction_dataset_dir"], "maps", map_filename)
        )

        self.animator = Animator(
            lanelet_map_file,
            self.egovehicle.id,
            self.egovehicle.appearance.color,
            ground_truth.vehicles(),
            self.dt,
            imagery_data=imagery_data,
        )

        self.animator.init_spatiotemporal_plot(self.n, n_pin_past, n_pin_future)
        self.animator.init_motion_profile(self.n, n_pin_past, n_pin_future)

        self.func_animation = animation.FuncAnimation(self.animator.fig, self.animate, repeat=True)
        self.i_anim = 0

    def update(self):

        start = time.time()
        timestampdata = self.egovehicle.timestamps()[self.i_anim]
        self.animator.update_ego(timestampdata, i=0, magnitude_flag=self.animator.frame.magnitude_flag)
        self.animator.update_others_cartesian(timestampdata, i=self.i_anim)
        self.animator.update_others_frenet(timestampdata, i=self.i_anim)
        self.animator.update_timestamp_text(timestampdata.timestamp)
        end = time.time()

        # print "It took %f to update the plot" % (end - start)

    def animation_index_counter(self):
        """
        increment the frame index counter
        """
        # increment the counter
        self.i_anim = (self.i_anim + 1) % len(self.egovehicle.timestamps)
        # raw_input("enter")

    def animate(self, *args, **kwargs):
        """
        We cannot use the incrementer embedded in FunctionAnimation even when we use the
        'frames' keyword in FuncAnimation to set an upper bound to the animation steps.
        Because, while the animation is paused, the counter in FuncAnimation continues to
        increment and hence, when returned back, there won't be continuity on the plotted
        on the figure or the printed values on the terminal. Therefore, we define our
        animation function not as 'animate(i_anim)' but as 'animate(_)' and implement our own counter.
        We increment i_anim' at the end of each animation-step, when the animation is not paused.
        If we would still use 'animate(i)' while using our own incrementer, our 'i_anim' would
        be overwritten by the FuncAnimation, which increments the 'i_anim' value even if
        the animation is paused. So, the argument of 'animate()' is determined by the FuncAnimation
        and the only solution is to define 'i_anim' externally
        """

        if not self.animator.frame.pause_flag:
            """
            if the animation is not paused:
             * increment the counter 'i' by one.
             * print the terminal outputs
            """
            self.update()
            self.animation_index_counter()

            """
            self.print_info()

            if self.video_saved:
                # Start printing once the 'video_saved' flag is set
                print "\n"

                # Non-standart console output:
                print "\033[1m%-2s %2i\033[0m\n" %("TIMESTEP:", self.i_anim)
            """

        if self.animator.frame.save_figure_flag:
            self.animator.frame.save_animation_instance(self.save_dir, self.i_anim)

    @staticmethod
    def show():
        plt.show()


if __name__ == "__main__":
    directory = sys.argv[1]
    settings, vehicles, map_data, save_dir, combination_id, current_time, _ = request_input2visualize(directory)

    animate_multi = AnimateMulti(map_data, save_dir, vehicles, settings, combination_id)
    animate_multi.show()