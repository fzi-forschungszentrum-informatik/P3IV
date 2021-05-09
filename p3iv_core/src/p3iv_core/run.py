# -*- coding: utf-8 -*-
from __future__ import division
import os
import pickle
import time
from pyfiglet import Figlet
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
from p3iv_core.configurations.test_cases import test_cases
from p3iv_core.configurations.utils import load_configurations


def run(configurations, f_execute=drive):

    # Print system time
    Print2Console.p("ss", ["Analysis start time:", time.ctime()], style="bright")

    # Print settings
    Print2Console.p("s", ["=" * 72], style="magenta", bold=True)
    Print2Console.p("s", ["Simulation configurations:"], style="magenta", bold=True)
    Print2Console.p("s", ["=" * 72], style="magenta", bold=True)
    pprint(configurations)

    # Load lanelet2 map
    maps_dir = os.path.join(configurations["interaction_dataset_dir"], "maps")
    laneletmap = lanelet_map_reader(configurations["map"], maps_dir=maps_dir)

    # Get ground-truth object data
    if configurations["source"] == "interaction_sim":
        from p3iv_core.bindings import InteractionDatasetBindings

        bindings = InteractionDatasetBindings(
            configurations["map"], configurations["interaction_dataset_dir"], configurations["temporal"]["dt"]
        )
        environment_model = bindings.get_environment_model(configurations["timestamp_begin"])
        ground_truth = bindings.create_ground_truth(environment_model.objects(), laneletmap, configurations)
        assert configurations["vehicle_of_interest"] in ground_truth.keys()
    else:
        raise Exception("Specify ground truth object data!")

    # Extract timestamps to be computed
    timestamps = range(
        configurations["timestamp_begin"], configurations["timestamp_end"] + 1, configurations["temporal"]["dt"]
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
            driven = o.timestamps.previous().plan_optimal.motion[1]
            o.timestamps.latest().state.position.mean = driven.cartesian.position.mean
            o.timestamps.latest().state.yaw.mean = driven.yaw_angle
            o.timestamps.latest().state.velocity.mean = driven.cartesian.velocity.mean

        elif configurations["simulation_type"] == "closed-loop":
            # closed-loop simulation
            # (ground truth object list remains the same; no new entries)
            for v in ground_truth.values():
                past_motion = v.timestamps.latest().motion[1:]
                # planned trajectory includes past three points and the current;
                # Those extra three points are trimmed away in Plan().
                # Therefore, take the first element in the motion array.
                driven = v.timestamps.latest().plan_optimal.motion[1]
                v.timestamps.create_and_add(ts_now)
                o.timestamps.latest().state.position.mean = driven.cartesian.position.mean
                o.timestamps.latest().state.yaw.mean = driven.yaw_angle
                o.timestamps.latest().state.velocity.mean = driven.cartesian.velocity.mean
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

                # plot results
                curr_save_dir = os.path.join(configurations["save_dir"], str(ts_now), str(vehicle.v_id))
                os.makedirs(curr_save_dir)

                # Update vehicle data
                ground_truth.update(vehicle)
            except:
                traceback.print_exc()
                msg = "Simulation terminated before timestamp " + str(configurations["timestamp_end"])
                msg += "\nThere may be a problem in calculations. "
                msg += "\nMaybe the vehicle has reached its destination?"
                print colored(msg, "red")
                break
        else:
            continue
        break

    Print2Console.p("s", ["=" * 72], style="magenta", bold=True)
    Print2Console.p("s", ["Simulation completed!"], style="magenta", bold=True)
    Print2Console.p("s", ["=" * 72], style="magenta", bold=True)
    return ground_truth