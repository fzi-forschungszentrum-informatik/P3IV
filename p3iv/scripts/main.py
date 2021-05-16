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
from p3iv_core.configurations.utils import load_configurations
from p3iv_core.run import run


def load_results(output_path):
    path_pickle = os.path.join(output_path, "results.pickle")
    with open(path_pickle, "rb") as input_file:
        gt = pickle.load(input_file)

    path_configurations = os.path.join(output_path, "configurations.json")
    with open(path_configurations) as json_file:
        configurations = json.load(json_file)
    return gt, configurations


if __name__ == "__main__":

    import argparse
    import json

    header = (
        "Probabilistic Prediction and Planning for Intelligent Vehicles Simulator\n"
        + "(c) FZI Forschungszentrum Informatik\n"
        + "Author: Ömer Şahin Taş and Others \n\n"
    )
    print(Figlet(font="slant").renderText("P3IV"))
    print(header)

    def SimulationTestCase(test_case):
        try:
            configurations = load_configurations(str(test_case))
        except:
            raise argparse.ArgumentTypeError(
                "Test-case invalid!\n \
                    For valid test cases see 'p3iv/src/p3iv/configurations/test_cases.py'"
            )
        return configurations

    def PredictionCase(test_case):
        try:
            configurations = load_configurations(str(test_case))

            # overwrite 'simulation type' and 'planner type' in prediction
            configurations["simulation_type"] = "open-loop"
            _v_id = configurations["vehicle_of_interest"]
            configurations["planning_meta"][_v_id] = (configurations["planning_meta"][_v_id][0], "default")
        except:
            raise argparse.ArgumentTypeError(
                "Test-case invalid!\n \
                    For valid test cases see 'p3iv/src/p3iv/configurations/test_cases.py'"
            )
        return configurations

    def TimestampKey(timestamp):
        if not timestamp:
            raise argparse.ArgumentTypeError("Please provide a timestamp with '--show-single'!")
        return int(timestamp)

    def SimulationResultsDir(results_dir):
        if not results_dir:
            raise argparse.ArgumentTypeError("Please provide a valid output dir")
        try:
            gt, configurations = load_results(results_dir)
        except:
            raise argparse.ArgumentTypeError("Output file not found!")
        return [gt, configurations]

    parser = argparse.ArgumentParser(description="Planning simulation environment.")
    parser.add_argument(
        "-r",
        "--run",
        action="store",
        type=SimulationTestCase,
        help="Run simulations for the config-file. \
                             \nUsage: --run=<test_case>",
    )
    parser.add_argument(
        "-p",
        "--predict",
        action="store",
        type=PredictionCase,
        help="Run prediction for the config-file. \
                             \nUsage: --predict=<test_case>",
    )
    parser.add_argument(
        "-ss",
        "--show-single",
        action="store",
        metavar="",
        type=TimestampKey,
        help="Show single-timestamp results of the simulation-run.\
                            Must be provided together with timestamp value. \
                            Usage: '--show-single=<integer>",
    )
    parser.add_argument(
        "-sm", "--show-multi", action="store_true", help="Show all-timestamp results of the simulation-run"
    )
    parser.add_argument(
        "-i",
        "--input",
        action="store",
        type=SimulationResultsDir,
        help="Show results from file. If not provided, \
                        the latest results from the output directory will be displayed. "
        "Usage: --input=<path_to_file>",
    )
    args = parser.parse_args()

    if args.run:

        # set default logger
        logging.basicConfig(level=logging.INFO)

        # create output dirs
        output_dir = create_output_dir()
        output_path = create_output_path(output_dir)

        # will serve as save directory for figures
        configurations = args.run
        configurations["save_dir"] = str(output_path)

        # run simulation
        gt = run(configurations, f_execute=drive)

        # save results
        filename_pickle = os.path.join(output_path, "results.pickle")
        gt.dump(filename_pickle)

        # save configurations as well
        filename_json = os.path.join(output_path, "configurations.json")
        j = json.dumps(configurations, indent=4)
        f = open(filename_json, "w")
        print >> f, j
        f.close()
        print("Completed!")

    elif args.predict:

        # set default logger
        logging.basicConfig(level=logging.INFO)

        # create output dirs
        output_dir = create_output_dir()
        output_path = create_output_path(output_dir)

        # will serve as save directory for figures
        configurations = args.predict
        configurations["save_dir"] = str(output_path)

        # run simulation
        gt = run(configurations, f_execute=predict)
        # save results
        filename_pickle = os.path.join(output_path, "results.pickle")
        gt.dump(filename_pickle)

        # save configurations as well
        filename_json = os.path.join(output_path, "configurations.json")
        j = json.dumps(configurations, indent=4)
        f = open(filename_json, "w")
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
            result_date_dir = "./../outputs"
            latest_date = sorted(os.listdir(result_date_dir))[-1]
            time_dir = os.path.join(result_date_dir, latest_date)
            latest_time_dir = sorted(os.listdir(time_dir))[-1]
            results_dir = os.path.realpath(os.path.join(time_dir, latest_time_dir))
            Print2Console.p("s", ["Displaying results from:"], style="magenta")
            Print2Console.p("s", [results_dir], style="magenta")
            Print2Console.p("s", ["Press enter to continue"], style="magenta", bold=True)
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
            from p3iv_visualization.animations.animate_multi import AnimateMulti

            animation = AnimateMulti(gt, configurations)
            animation.show()
            animation.animate()
            print("Completed!")

        else:
            sys.exit(1)
    else:
        parser.print_help()
