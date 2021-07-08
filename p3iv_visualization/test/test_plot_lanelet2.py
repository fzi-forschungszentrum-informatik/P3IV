# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import os
import unittest
from matplotlib import pyplot as plt
from p3iv_visualization.lanelet2.plot_map import PlotLanelet2Map


def variant1(ax, lanelet_map_path):
    # Option 1: without background imagery
    PlotLanelet2Map(ax, lanelet_map_path)
    plt.show()


def variant2(ax, path_this_file, lanelet_map_path, lanelet_map_name):
    # Option 2: with background imagery
    fig, ax = plt.subplots(1, 1)
    imagery_file = lanelet_map_name + ".png"
    imagery_file_path = os.path.join(path_this_file, "../src/p3iv_visualization/res/", imagery_file)
    imagery = [imagery_file_path, 932, 1067, 942, 1036]
    PlotLanelet2Map(ax, lanelet_map_path, imagery_data=imagery)
    plt.show()


class PlotLanelet2Test(unittest.TestCase):
    def test_plot_vehicle(self):
        print("running...")
        fig, ax = plt.subplots(1, 1)
        path_this_file = os.path.dirname(os.path.realpath(__file__))
        lanelet_map_name = "DR_DEU_Roundabout_OF"
        lanelet_map_file = lanelet_map_name + ".osm"
        lanelet_map_path = os.path.join(path_this_file, "../src/p3iv_visualization/res/", lanelet_map_file)

        variant1(ax, lanelet_map_path)
        variant2(ax, path_this_file, lanelet_map_path, lanelet_map_name)


class PlotLaneletMap(unittest.TestCase):
    def test_laneletmap(self):
        fig, ax = plt.subplots(1, 1)
        p = PlotLanelet2Map(ax, "SanFrancisco-Downtown-Sample-Lanelet2", lat_origin=37.787, lon_origin=-122.406)
        plt.show()


if __name__ == "__main__":
    unittest.main()
