#!/usr/bin/env python

import lanelet2
import os


def lanelet_map_reader(laneletmap, maps_dir=None):

    if not maps_dir:
        # use internally stored maps in res
        maps_dir_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../res/maps/lanelet2")
        maps_dir = os.path.normpath(maps_dir_)

    error_string = ""
    lanelet_map_ending = ".osm"
    lanelet_map_file = maps_dir + "/" + laneletmap + lanelet_map_ending

    if not os.path.isfile(lanelet_map_file):
        error_string += 'Did not find lanelet map file "' + lanelet_map_file + '"\n'
    if error_string != "":
        error_string += "Type --help for help."
        raise IOError(error_string)

    # load and draw the lanelet2 map, either with or without the lanelet2 library
    lat_origin = 0.0  # origin is necessary to correctly project the lat lon values in the osm file to the local
    lon_origin = 0.0  # coordinates in which the tracks are provided; we decided to use (0|0) for every scenario
    print(("\nLoading map : ", str(laneletmap)))

    projector = lanelet2.projection.UtmProjector(lanelet2.io.Origin(lat_origin, lon_origin))
    laneletmap = lanelet2.io.load(lanelet_map_file, projector)

    return laneletmap
