from __future__ import division

import pickle
import time
from datetime import datetime
from pprint import pprint
import sys
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
    if configurations["interaction_sim"]:
        from mp_sim.bindings.interaction_dataset import use_interaction_sim_data, create_simulation_objects
        situation = use_interaction_sim_data(configurations)
        ground_truth_objects = create_simulation_objects(situation.tracked_objects.values(), laneletmap, configurations)
    else:
        raise Exception("Specify ground truth object data!")

    sampling_time = int(configurations['temporal']['dt'])
    timestamps = [configurations['timestamp_begin'] + i * sampling_time for i in range(0, configurations['main']['NN'])]

    #vehicles = create_objects(parsed_xml_data, map_data, instance_settings["Main"]["dt"], N_TOTAL, instance_settings)
    #vehicles = list(vehicles)

    # Perform computation
    for ts_now in timestamps:
        # Print information
        Print2Console.p('s', ['='*72], style='magenta', bold=True)
        Print2Console.p('sf', ['Computing timestamp:', ts_now], first_col_w=38, style='magenta', bold=True)
        Print2Console.p('s', ['='*72], style='magenta', bold=True)

        # Compute the trajectory of vehicles
        for vehicle in ground_truth_objects:
            print "v: ", vehicle
            vehicles = drive(vehicle, ground_truth_objects, laneletmap, configurations['save_dir'], ts_now)


if __name__ == '__main__':

    output_dir = create_output_dir()
    output_path = create_output_path(output_dir)

    if len(sys.argv) == 2:
        test_case = sys.argv[1]
        configurations = load_configurations(output_path, test_case)
        run(configurations)
    else:
        print 'Too low/many arguments. Specify a test case (see src/configurations/test_cases.py)'
        sys.exit(1)
