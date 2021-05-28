import os
from matplotlib import pyplot as plt
from p3iv_visualization.lanelet2.plot_map import PlotLanelet2Map


def variant1(lanelet_map_path):
    # Option 1: without background imagery
    PlotLanelet2Map(ax, lanelet_map_path)
    plt.show()


def variant2(lanelet_map_path, lanelet_map_name):
    # Option 2: with background imagery
    fig, ax = plt.subplots(1, 1)
    imagery_file = lanelet_map_name + ".png"
    imagery_file_path = os.path.join(path_this_file, "../../../p3iv_utils/res/maps/lanelet2", imagery_file)
    imagery = [imagery_file_path, 932, 1067, 942, 1036]
    PlotLanelet2Map(ax, lanelet_map_path, imagery_data=imagery)
    plt.show()


if __name__ == "__main__":
    print("running...")
    fig, ax = plt.subplots(1, 1)
    path_this_file = os.path.dirname(os.path.realpath(__file__))
    lanelet_map_name = "DR_DEU_Roundabout_OF"
    lanelet_map_file = lanelet_map_name + ".osm"
    lanelet_map_path = os.path.join(path_this_file, "../../../p3iv_utils/res/maps/lanelet2", lanelet_map_file)

    variant1(lanelet_map_path)
    variant2(lanelet_map_path, lanelet_map_name)
