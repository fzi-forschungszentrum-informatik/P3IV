# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import lanelet2
import os


def load_lanelet2_map(lanelet_map_file, lat_origin=0.0, lon_origin=0.0):
    # load the lanelet2 map
    projector = lanelet2.projection.UtmProjector(lanelet2.io.Origin(lat_origin, lon_origin))
    # lanelet2 C++ interface requires basic string. Cast unicode to string.
    return lanelet2.io.load(str(lanelet_map_file), projector)


def lanelet_map_reader(laneletmap, maps_dir=None, lat_origin=0.0, lon_origin=0.0, **kwargs):
    """
    Read lanelet2 map.

    Can of accept one of the below as 'laneletmap' argument:
    - map name
    - map name with type ending
    - map path

    :param laneletmap: Lanelet2 map instance or Lanelet2 map path
    :type laneletmap: lanelet2.core.LaneletMap / string
    """

    if isinstance(laneletmap, lanelet2.core.LaneletMap):
        return laneletmap

    print("\nRead map: ", str(laneletmap))

    if os.path.isfile(laneletmap):
        return load_lanelet2_map(laneletmap, lat_origin, lon_origin)

    # if maps_dir is not given, use internally stored maps in res
    if not maps_dir:
        maps_dir_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../res/maps/lanelet2")
        maps_dir = os.path.normpath(maps_dir_)

    # join maps_dir
    laneletmap = os.path.join(maps_dir, laneletmap)

    # if laneletmap is still not valid, add ".osm" suffix
    if not os.path.isfile(laneletmap):
        lanelet_map_ending = ".osm"
        laneletmap = laneletmap + lanelet_map_ending

    return load_lanelet2_map(laneletmap, lat_origin, lon_origin)


def get_lanelet_map(configurations):
    """
    Get lanelet map based on type of simulation which is defined in simulation configurations.
    """

    # determine path of the lanelet map
    if configurations["source"] == "interaction_sim":
        # read INTERACTION dataset maps and records
        maps_dir = os.path.join(configurations["dataset"], "maps")
    elif configurations["source"] == "d_sim":
        # read rounD dataset maps and records
        maps_dir = os.path.join(configurations["dataset"], "lanelets")
    else:
        # read custom Lanelet map
        maps_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../res/maps/lanelet2")

    # read origin of the map
    lat, lon = configurations["map_coordinate_origin"]

    # Load lanelet2 map
    laneletmap = lanelet_map_reader(configurations["map"], maps_dir=maps_dir, lat_origin=lat, lon_origin=lon)

    return laneletmap
