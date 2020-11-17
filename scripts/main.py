from __future__ import division
import os
import pickle
import time
from datetime import datetime
from pprint import pprint
import sys
import logging
import traceback
import itertools
import shutil
###
from mp_sim.configurations.test_cases import test_cases

from util_simulation.output.consoleprint import Print2Console
from util_simulation.output.utils import create_output_dir, create_output_path, save_settings
from util_simulation.map.lanelet_map_reader import lanelet_map_reader
from util_simulation.vehicle.main import Vehicle
from mp_sim.drive import drive
from mp_sim.configurations.utils import load_configurations
#from postprocessing.postprocessing_plots import do_post_plots
#from sim_master.test_cases import test_cases
#from map_data.main import main as get_map
#from sim_master.vehicle.create_vehicle import create_objects


def run(configurations, instance_settings=None, subdir='', subdir_postfix=''):

    # Print system time
    Print2Console.p('ss', ['Analysis start time:', time.ctime()], style='bright')

    # Print settings
    Print2Console.p('s', ['='*72],                       style='magenta', bold=True)
    Print2Console.p('s', ['Simulation configurations:'], style='magenta', bold=True)
    Print2Console.p('s', ['='*72],                       style='magenta', bold=True)
    pprint(configurations)

    # Load lanelet2 map
    laneletmap = lanelet_map_reader(configurations["map"])

    # Get ground-truth object data
    if configurations['source'] == 'interaction_sim':
        from mp_sim.bindings.interaction_dataset import InteractionDatasetBindings
        bindings = InteractionDatasetBindings(configurations, laneletmap)
        scene_model = bindings.get_scene_model(configurations["timestamp_begin"])
        ground_truth = bindings.create_ground_truth(scene_model.tracked_objects(), laneletmap, configurations)

    else:
        raise Exception("Specify ground truth object data!")

    # Extract timestamps to be computed
    timestamps = range(configurations['timestamp_begin'], configurations['timestamp_end'] + 1, configurations['temporal']['dt'])

    # Perform computation
    for i, ts_now in enumerate(timestamps):
        # Print information
        Print2Console.p('s', ['='*72], style='magenta', bold=True)
        Print2Console.p('sf', ['Computing timestamp:', ts_now], first_col_w=38, style='magenta', bold=True)
        Print2Console.p('s', ['='*72], style='magenta', bold=True)

        if configurations['open_loop'] or i == 0:
            bindings.update_simulation_objects_motion(ground_truth, ts_now)
        else:
            # closed-loop simulation
            for v in ground_truth.values():
                past_motion = v.timestamps.latest().motion
                driven_motion = v.timestamps.latest().plan_optimal.motion[4]  # the first three were already driven
                v.timestamps.create_and_add(ts_now)
                v.timestamps.latest().motion = past_motion
                v.timestamps.latest().motion.append(driven_motion)

        # Compute the trajectory of vehicles who have a 'toLanelet' in their **objective**!
        for vehicle in [_v for _v in ground_truth.vehicles() if _v.objective.toLanelet]:
            drive(vehicle, ground_truth)

            # plot results
            curr_save_dir = os.path.join(configurations['save_dir'], str(ts_now), str(vehicle.v_id))
            os.makedirs(curr_save_dir)
            #plot_prediction(situation_model.objects, vehicle.vehicle_id, settings["Main"]["N"], settings["Main"]["dt"], curr_save_dir)
            #plot_planning(vehicle, current_time, lightsaber_base, settings)

            # Update vehicle data
            ground_truth.update(vehicle)

    Print2Console.p('s', ['='*72], style='magenta', bold=True)
    Print2Console.p('s', ['Simulation completed!'], style='magenta', bold=True)
    Print2Console.p('s', ['='*72], style='magenta', bold=True)

    return ground_truth


def load_results(output_path):
    path_pickle = os.path.join(output_path, "results.pickle")
    with open(path_pickle, "rb") as input_file:
        gt = pickle.load(input_file)

    path_configurations = os.path.join(output_path, "configurations.json")
    with open(path_configurations) as json_file:
        configurations = json.load(json_file)
    return gt, configurations


if __name__ == '__main__':

    import argparse
    import json

    parser = argparse.ArgumentParser(description='Planning simulation environment.')
    parser.add_argument("config", type=str, help="Test case (see mp_sim/src/mp_sim/configurations/test_cases.py) "
                                                 "or pickle file of simulation-results ")
    parser.add_argument("-r", "--run", action="store_true", help="Run simulations for the config-file")
    parser.add_argument("-ss", "--show-single", action='store', metavar='', type=int,
                        help="Show single-timestamp results of the simulation-run. Must be provided together with "
                             "timestamp value, i.e. '--show-single=<integer>")
    parser.add_argument("-sm", "--show-multi", action="store_true",
                        help="Show all-timestamp results of the simulation-run")
    args = parser.parse_args()

    # create output dirs
    output_dir = create_output_dir()
    output_path = create_output_path(output_dir)

    if args.run:
        # set default logger
        logging.basicConfig(level=logging.INFO)
        test_case = sys.argv[1]
        configurations = load_configurations(output_path, test_case)
        gt = run(configurations)
        filename_pickle = os.path.join(output_path, "results.pickle")
        gt.dump(filename_pickle)

        # save configurations as well
        filename_json = os.path.join(output_path, "configurations.json")
        j = json.dumps(configurations, indent=4)
        f = open(filename_json, 'w')
        print >> f, j
        f.close()
        print("Completed!")

    elif args.show_single:
        from visualization.animations.animate_single import AnimateSingle
        timestamp = str(args.show_single)
        gt, configurations = load_results(sys.argv[1])

        animation = AnimateSingle(gt, configurations, timestamp)
        animation.show()
        animation.animate()
        print("Completed!")

    elif args.show_multi:
        from visualization.animations.animate_multi import AnimateMulti
        gt, configurations = load_results(sys.argv[1])

        animation = AnimateMulti(gt, configurations)
        animation.show()
        animation.animate()
        print("Completed!")

    else:
        sys.exit(1)
