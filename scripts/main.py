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
from mp_sim.configurations.test_cases import test_cases
from util_simulation.output.consoleprint import Print2Console
from util_simulation.output.utils import create_output_dir, create_output_path, save_settings
from util_simulation.map.lanelet_map_reader import lanelet_map_reader
from util_simulation.vehicle.main import Vehicle
from mp_sim.execute import drive
from mp_sim.configurations.utils import load_configurations


def run(configurations, instance_settings=None, subdir='', subdir_postfix=''):

    # Print system time
    Print2Console.p('ss', ['Analysis start time:',
                           time.ctime()], style='bright')

    # Print settings
    Print2Console.p('s', ['='*72],
                    style='magenta', bold=True)
    Print2Console.p('s', ['Simulation configurations:'],
                    style='magenta', bold=True)
    Print2Console.p('s', ['='*72],
                    style='magenta', bold=True)
    pprint(configurations)

    # Load lanelet2 map
    laneletmap = lanelet_map_reader(configurations["map"])

    # Get ground-truth object data
    if configurations['source'] == 'interaction_sim':
        from mp_sim.bindings import InteractionDatasetBindings
        bindings = InteractionDatasetBindings(
            configurations["map"], configurations['temporal']['dt'])
        environment_model = bindings.get_environment_model(
            configurations["timestamp_begin"])
        ground_truth = bindings.create_ground_truth(
            environment_model.objects(), laneletmap, configurations)
        assert (configurations['vehicle_of_interest'] in ground_truth.keys())
    else:
        raise Exception("Specify ground truth object data!")

    # Extract timestamps to be computed
    timestamps = range(configurations['timestamp_begin'],
                       configurations['timestamp_end'] + 1,
                       configurations['temporal']['dt'])

    # Perform computation
    for i, ts_now in enumerate(timestamps):
        # Print information
        Print2Console.p('s', ['='*72], style='magenta', bold=True)
        Print2Console.p('sf', ['Computing timestamp:', ts_now],
                        first_col_w=38, style='magenta', bold=True)
        Print2Console.p('s', ['='*72], style='magenta', bold=True)

        # update planned motion from previous solution or from dataset
        if configurations['simulation_type'] == "open-loop" or i == 0:
            # update ground truth objects
            bindings.update_open_loop_simulation(
                ground_truth, ts_now, laneletmap, configurations)

        elif configurations['simulation_type'] == "semi-open-loop":
            # update ground truth objects
            bindings.update_open_loop_simulation(
                ground_truth, ts_now, laneletmap, configurations)

            o = ground_truth[configurations['vehicle_of_interest']]
            past_motion = o.timestamps.previous().motion[1:]
            driven = o.timestamps.previous().plan_optimal.motion[1]
            o.timestamps.latest().motion = past_motion
            o.timestamps.latest().motion.append(driven)

        elif configurations['simulation_type'] == "closed-loop":
            # closed-loop simulation
            # (ground truth object list remains the same; no new entries)
            for v in ground_truth.values():
                past_motion = v.timestamps.latest().motion[1:]
                # planned trajectory includes past three points and the current;
                # Those extra three points are trimmed away in Plan().
                # Therefore, take the first element in the motion array.
                driven = v.timestamps.latest().plan_optimal.motion[1]
                v.timestamps.create_and_add(ts_now)
                v.timestamps.latest().motion = past_motion
                v.timestamps.latest().motion.append(driven)
        else:
            msg = "'simulation_type' in configurations is wrong." + \
                  "Choose between 'open-loop' / 'closed-loop' / 'semi-open-loop'"
            raise Exception(msg)

        # Compute the trajectory of vehicles who have a 'toLanelet' in their **objective**!
        for vehicle in [_v for _v in ground_truth.vehicles() if _v.objective.toLanelet]:
            try:
                drive(vehicle, ground_truth)

                # plot results
                curr_save_dir = os.path.join(
                    configurations['save_dir'], str(ts_now), str(vehicle.v_id))
                os.makedirs(curr_save_dir)
                #plot_prediction(situation_model.objects, vehicle.vehicle_id, settings["Main"]["N"], settings["Main"]["dt"], curr_save_dir)
                #plot_planning(vehicle, current_time, lightsaber_base, settings)

                # Update vehicle data
                ground_truth.update(vehicle)
            except:
                traceback.print_exc()
                msg = "Simulation terminated before timestamp " + \
                    str(configurations['timestamp_end'])
                msg += "\nThere may be a problem in calculations. "
                msg += "\nMaybe the vehicle has reached its destination?"
                print colored(msg, 'red')
                break
        else:
            continue
        break

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
    header = "Probabilistic Prediction and Planning for Intelligent Vehicles Simulator\n" + \
        "(c) FZI Forschungszentrum Informatik\n" + \
        "Author: Ömer Şahin Taş and Others \n\n"
    print Figlet(font='slant').renderText('P3IV')
    print header

    def SimulationTestCase(test_case):
        try:
            configurations = load_configurations(str(test_case))
        except:
            raise argparse.ArgumentTypeError(
                "Test-case invalid!\n \
                    For valid test cases see 'mp_sim/src/mp_sim/configurations/test_cases.py'")
        return configurations

    def TimestampKey(timestamp):
        if not timestamp:
            raise argparse.ArgumentTypeError(
                "Please provide a timestamp with '--show-single'!")
        return int(timestamp)

    def SimulationResultsDir(results_dir):
        if not results_dir:
            raise argparse.ArgumentTypeError(
                "Please provide a valid output dir")
        try:
            gt, configurations = load_results(results_dir)
        except:
            raise argparse.ArgumentTypeError("Output file not found!")
        return [gt, configurations]

    parser = argparse.ArgumentParser(
        description='Planning simulation environment.')
    parser.add_argument("-r", "--run", action="store", type=SimulationTestCase,
                        help="Run simulations for the config-file. \
                             \nUsage: --run=<test_case>")
    parser.add_argument("-ss", "--show-single", action='store', metavar='', type=TimestampKey,
                        help="Show single-timestamp results of the simulation-run.\
                            Must be provided together with timestamp value. \
                            Usage: '--show-single=<integer>")
    parser.add_argument("-sm", "--show-multi", action="store_true",
                        help="Show all-timestamp results of the simulation-run")
    parser.add_argument("-i", "--input", action="store", type=SimulationResultsDir,
                        help="Show results from file. If not provided, \
                        the latest results from the output directory will be displayed. "
                             "Usage: --input=<path_to_file>")
    args = parser.parse_args()

    if args.run:

        # set default logger
        logging.basicConfig(level=logging.INFO)

        # create output dirs
        output_dir = create_output_dir()
        output_path = create_output_path(output_dir)

        # will serve as save directory for figures
        configurations = args.run
        configurations['save_dir'] = str(output_path)

        # run simulation
        gt = run(configurations)

        # save results
        filename_pickle = os.path.join(output_path, "results.pickle")
        gt.dump(filename_pickle)

        # save configurations as well
        filename_json = os.path.join(output_path, "configurations.json")
        j = json.dumps(configurations, indent=4)
        f = open(filename_json, 'w')
        print >> f, j
        f.close()
        print("Completed!")

    elif args.show_single or args.show_multi:
        # load results & visualize
        if args.input:
            gt, configurations = args.input
        else:
            # no simulation results file is provided; load latest results
            gt, configurations = None, None
            result_date_dir = "./../../../outputs"
            latest_date = sorted(os.listdir(result_date_dir))[-1]
            time_dir = os.path.join(result_date_dir, latest_date)
            latest_time_dir = sorted(os.listdir(time_dir))[-1]
            results_dir = os.path.join(time_dir, latest_time_dir)
            Print2Console.p('s', ['Displaying results from:'], style='magenta')
            Print2Console.p('s', [results_dir], style='magenta')
            Print2Console.p('s', ["Press enter to continue"],
                            style='magenta', bold=True)
            raw_input("")
            gt, configurations = load_results(results_dir)

        if args.show_single:
            from visualization.animations.animate_single import AnimateSingle
            timestamp = str(args.show_single)
            animation = AnimateSingle(gt, configurations, timestamp)
            animation.show()
            animation.animate()
            print("Completed!")

        elif args.show_multi:
            from visualization.animations.animate_multi import AnimateMulti
            animation = AnimateMulti(gt, configurations)
            animation.show()
            animation.animate()
            print("Completed!")

        else:
            sys.exit(1)
    else:
        parser.print_help()
