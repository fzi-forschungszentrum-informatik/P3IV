from __future__ import division
import os
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
    if configurations['source'] == 'interaction_sim':
        from mp_sim.bindings.interaction_dataset import InteractionDatasetBindings
        bindings = InteractionDatasetBindings(configurations, laneletmap)
        scene_model = bindings.get_scene_model(configurations["timestamp_begin"])
        ground_truth = bindings.create_simulation_objects(scene_model.tracked_objects.values(), laneletmap, configurations)

    else:
        raise Exception("Specify ground truth object data!")

    sampling_time = int(configurations['temporal']['dt'])
    timestamps = [configurations['timestamp_begin'] + i * sampling_time for i in range(0, configurations['main']['NN'])]

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
                driven_motion = v.timestamps.latest().motion_plans[0].motion[0]
                v.timestamps.create_and_add(ts_now)
                v.timestamps.latest().motion = past_motion
                v.timestamps.latest().motion.append(driven_motion)

        # Compute the trajectory of vehicles who have a 'toLanelet' in their **objective**!
        for vehicle in [_v for _v in ground_truth.vehicles() if _v.objective.route]:
            drive(vehicle, ground_truth)

            # plot results
            curr_save_dir = os.path.join(configurations['save_dir'], str(ts_now), str(vehicle.v_id))
            os.makedirs(curr_save_dir)
            #plot_prediction(situation_model.objects, vehicle.vehicle_id, settings["Main"]["N"], settings["Main"]["dt"], curr_save_dir)
            #plot_planning(vehicle, current_time, lightsaber_base, settings)

            # Update vehicle data
            ground_truth.update(vehicle)

    return ground_truth


if __name__ == '__main__':

    output_dir = create_output_dir()
    output_path = create_output_path(output_dir)

    if len(sys.argv) == 2:
        test_case = sys.argv[1]
        configurations = load_configurations(output_path, test_case)
        run(configurations)
        Print2Console.p('s', ['='*72], style='magenta', bold=True)
        Print2Console.p('s', ['Simulation completed!'], style='magenta', bold=True)
        Print2Console.p('s', ['='*72], style='magenta', bold=True)
    else:
        print 'Too low/many arguments. Specify a test case (see src/configurations/test_cases.py)'
        sys.exit(1)
