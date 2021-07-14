# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import os
import unittest
from matplotlib import pyplot as plt
from p3iv_visualization.cartesian.plot_cartesian import PlotCartesian


class Appearance(object):
    def __init__(self, color, width, length):
        self.color = color
        self.width = width
        self.length = length


class Vehicle(object):
    def __init__(self, v_id, color, width, length):
        self.id = v_id
        self.appearance = Appearance(color, width, length)


def example_with_vehicles(ax, lanelet_map_path):
    p = PlotCartesian(ax, lanelet_map_path)
    v1 = Vehicle(1, "red", 2.2, 4.0)
    v2 = Vehicle(2, "blue", 2.2, 4.0)
    vehicles = {1: v1, 2: v2}

    p.fill_vehicles(list(vehicles.values()))
    p.set_vehicle_plots()
    p.update_vehicle_plot(1, 997, 1012, 15, 10.0)
    p.update_vehicle_plot(2, 986, 1005, 60, 10.0)
    plt.show()


class PlotCartesianTest(unittest.TestCase):
    def test_plot_vehicle(self):
        print("running...")
        fig, ax = plt.subplots(1, 1)
        path_this_file = os.path.dirname(os.path.realpath(__file__))
        lanelet_map_name = "DR_DEU_Roundabout_OF"
        lanelet_map_file = lanelet_map_name + ".osm"
        lanelet_map_path = os.path.join(path_this_file, "../src/p3iv_visualization/res/", lanelet_map_file)

        example_with_vehicles(ax, lanelet_map_path)


if __name__ == "__main__":
    unittest.main()
