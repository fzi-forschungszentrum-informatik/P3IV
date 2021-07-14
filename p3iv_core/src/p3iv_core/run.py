# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import os
import pickle
import time
from datetime import datetime
from pprint import pprint
import sys
import logging
import traceback
from termcolor import colored
import itertools
import shutil
from p3iv_utils.consoleprint import Print2Console
from p3iv_utils.ofstream import create_output_dir, create_output_path, save_settings
from p3iv_utils.lanelet_map_reader import lanelet_map_reader
from p3iv_types.vehicle import Vehicle
from p3iv_modules.execute import drive, predict
from p3iv_core.configurations.utils import load_configurations


def run(configurations, f_execute=drive):

    # Print system time
    Print2Console.p("ss", ["Simulation start time:", time.ctime()], style="bright")

    # Print settings
    Print2Console.p("s", ["=" * 72], style="magenta", bold=True)
    Print2Console.p("s", ["Simulation configurations:"], style="magenta", bold=True)
    Print2Console.p("s", ["=" * 72], style="magenta", bold=True)
    pprint(configurations)

    # determine path of the lanelet map
    if configurations["source"] == "interaction_sim":
        # read INTERACTION dataset maps and records
        maps_dir = os.path.join(configurations["dataset"], "maps")
    elif configurations["source"] == "d_sim":
        # read rounD dataset maps and records
        maps_dir = os.path.join(configurations["dataset"], "lanelets")
    else:
        # read custom Lanelet map
        maps_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../p3iv_utils/res/maps/lanelet2")

    # read origin of the map
    lat, lon = configurations["map_coordinate_origin"]

    # Load lanelet2 map
    laneletmap = lanelet_map_reader(configurations["map"], maps_dir=maps_dir, lat_origin=lat, lon_origin=lon)

    # Get ground-truth object data
    if configurations["source"] == "interaction_sim":
        from p3iv_core.bindings import InteractionDatasetBindings

        bindings = InteractionDatasetBindings(
            configurations["map"],
            configurations["dataset"],
            configurations["track_file_number"],
            configurations["temporal"]["dt"],
        )
        environment_model = bindings.get_environment_model(configurations["timestamp_begin"])
        ground_truth = bindings.create_ground_truth(environment_model.objects(), laneletmap, configurations)
        assert configurations["vehicle_of_interest"] in list(ground_truth.keys())
    else:
        raise Exception("Specify ground truth object data!")

    # Extract timestamps to be computed
    timestamps = list(
        range(configurations["timestamp_begin"], configurations["timestamp_end"] + 1, configurations["temporal"]["dt"])
    )

    # Perform computation
    for i, ts_now in enumerate(timestamps):
        # Print information
        Print2Console.p("s", ["=" * 72], style="magenta", bold=True)
        Print2Console.p("sf", ["Computing timestamp:", ts_now], first_col_w=38, style="magenta", bold=True)
        Print2Console.p("s", ["=" * 72], style="magenta", bold=True)

        # update planned motion from previous solution or from dataset
        if configurations["simulation_type"] == "open-loop" or i == 0:
            # update ground truth objects
            bindings.update_open_loop_simulation(ground_truth, ts_now, laneletmap, configurations)

        elif configurations["simulation_type"] == "semi-open-loop":
            # update ground truth objects
            bindings.update_open_loop_simulation(ground_truth, ts_now, laneletmap, configurations)

            o = ground_truth[configurations["vehicle_of_interest"]]
            driven = o.timestamps.previous().plan_optimal.states[1]
            o.timestamps.latest().state.position.mean = driven.position.mean
            o.timestamps.latest().state.yaw.mean = driven.yaw.mean
            o.timestamps.latest().state.velocity.mean = driven.velocity.mean

        elif configurations["simulation_type"] == "closed-loop":
            # closed-loop simulation
            # (ground truth object list remains the same; no new entries)
            for v in list(ground_truth.values()):
                past_motion = v.timestamps.latest().motion[1:]
                # planned trajectory includes past three points and the current;
                # Those extra three points are trimmed away in Plan().
                # Therefore, take the first element in the motion array.
                driven = v.timestamps.latest().plan_optimal.motion[1]
                v.timestamps.create_and_add(ts_now)
                o.timestamps.latest().state.position.mean = driven.position.mean
                o.timestamps.latest().state.yaw.mean = driven.yaw.mean
                o.timestamps.latest().state.velocity.mean = driven.velocity.mean
        else:
            msg = (
                "'simulation_type' in configurations is wrong."
                + "Choose between 'open-loop' / 'closed-loop' / 'semi-open-loop'"
            )
            raise Exception(msg)

        # Compute the trajectory of vehicles who have a 'toLanelet' in their **objective**!
        for vehicle in [_v for _v in ground_truth.vehicles() if _v.objective.toLanelet]:
            try:
                f_execute(vehicle, ground_truth)

                # if you want to have plots after each timestamp, you can add them here
                curr_save_dir = os.path.join(configurations["save_dir"], str(ts_now), str(vehicle.id))
                os.makedirs(curr_save_dir)

                # Update vehicle data
                ground_truth.update(vehicle)
            except:
                traceback.print_exc()
                msg = "Simulation terminated before timestamp " + str(configurations["timestamp_end"])
                msg += "\nThere may be a problem in calculations. "
                msg += "\nMaybe the vehicle has reached its destination?"
                print(colored(msg, "red"))
                break
        else:
            continue
        break

    Print2Console.p("s", ["=" * 72], style="magenta", bold=True)
    Print2Console.p("s", ["Simulation completed!"], style="magenta", bold=True)
    Print2Console.p("s", ["=" * 72], style="magenta", bold=True)
    return ground_truth
