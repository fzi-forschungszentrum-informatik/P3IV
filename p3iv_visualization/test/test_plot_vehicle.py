from __future__ import division, absolute_import
import unittest
import os
import numpy as np
import matplotlib.pyplot as plt
from p3iv_visualization.cartesian.plot_vehicle import PlotVehicle


class PlotVehicleTest(unittest.TestCase):
    def test_plot_vehicle(self):
        fig, ax = plt.subplots(1, 1)
        path_file = os.path.dirname(os.path.realpath(__file__))
        path_img = os.path.join(path_file, "../src/p3iv_visualization/res/car.png")

        v1 = PlotVehicle(ax, 0, "blue")
        v1.create_track()
        v1.set_car_image(path_img)
        v1.set_car_patch()
        v1.set_uncertainty_ellipse()

        motion_past = np.zeros((10, 2))
        motion_past[:, 0] = np.arange(10)
        motion_future = np.zeros((12, 2))
        motion_future[:, 0] = np.arange(9, 21)
        current_x, current_y = 9, 0
        stop_x, stop_y = 15, 0

        v1.update_track(motion_past, motion_future)
        v1.update_car_image(current_x, current_y, 120)
        v1.update_speed_info_text(current_x, current_y, 10)
        v1.update_car_patch_center(current_x, current_y, 120)
        v1.update_uncertainty_ellipse(current_x, current_y, 120, [14, 6])

        visible_region_polys = [np.array([[0.0, 5.0], [10.0, 5.0], [15.0, 10.0], [15.0, 15.0], [0.0, 5.0]])]
        v1.update_visible_area(visible_region_polys)

        ax.set_xlim(0, 25)
        ax.set_ylim(-5, 5)
        ax.set_aspect("equal")

        v1.center_vehicle_in_plot(current_x, current_y, 15)

        plt.show()


if __name__ == "__main__":
    unittest.main()
