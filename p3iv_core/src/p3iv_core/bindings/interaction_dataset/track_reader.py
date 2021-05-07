#!/usr/bin/env python

import lanelet2
import os

from external import dataset_reader
from external import dict_utils


def track_reader(scenario_name, interaction_dataset_dir, track_file_number=0):

    tracks_dir = os.path.join(interaction_dataset_dir, "recorded_trackfiles")
    error_string = ""

    scenario_dir = tracks_dir + "/" + scenario_name
    track_file_prefix = "vehicle_tracks_"
    track_file_ending = ".csv"
    track_file_name = scenario_dir + "/" + track_file_prefix + str(track_file_number).zfill(3) + track_file_ending
    if not os.path.isdir(tracks_dir):
        error_string += 'Did not find track file directory "' + tracks_dir + '"\n'
    if not os.path.isdir(scenario_dir):
        error_string += 'Did not find scenario directory "' + scenario_dir + '"\n'
    if not os.path.isfile(track_file_name):
        error_string += 'Did not find track file "' + track_file_name + '"\n'
    if error_string != "":
        error_string += "Type --help for help."
        raise IOError(error_string)

    # load the tracks
    print("Loading tracks...")
    track_dictionary = dataset_reader.read_tracks(track_file_name)

    timestamp_min = 1e9
    timestamp_max = 0
    for key, track in dict_utils.get_item_iterator(track_dictionary):
        timestamp_min = min(timestamp_min, track.time_stamp_ms_first)
        timestamp_max = max(timestamp_max, track.time_stamp_ms_last)

    return track_dictionary


if __name__ == "__main__":
    from pprint import pprint

    t = track_reader("DR_DEU_Merging_MT")
    pprint(t)
    print("Test passed")
