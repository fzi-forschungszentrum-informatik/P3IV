#!/usr/bin/env python

import lanelet2
import os


def load_lanelet2_map(lanelet_map_file, lat_origin=0.0, lon_origin=0.0):
    # load the lanelet2 map
    projector = lanelet2.projection.UtmProjector(lanelet2.io.Origin(lat_origin, lon_origin))
    return lanelet2.io.load(lanelet_map_file, projector)


def lanelet_map_reader(laneletmap, maps_dir=None):
    """
    Read lanelet2 map.

    Can of accept one of the below as 'laneletmap' argument:
    - map name
    - map name with type ending
    - map path

    :param laneletmap: Lanelet2 map instance or Lanelet2 map path
    :type laneletmap: lanelet2.core.LaneletMap / string
    """
    print("\nRead map: ", str(laneletmap))

    if os.path.isfile(laneletmap):
        return load_lanelet2_map(laneletmap)

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

    return load_lanelet2_map(laneletmap)
