#!/usr/bin/python
from __future__ import division
import time
import os
import numpy as np
from collections import OrderedDict
from termcolor import colored, cprint
from understanding.main import Understand
from prediction.main import Predict
from prediction.situation_model import SituationModel
from mp_sim.bindings import InteractionDatasetBindings
from visualization.lanelet2.plot_map import PlotLanelet2Map
#from visualization.cartesian.plot_maneuver_path import PlotManeuverPath
from prediction.visualization.plot_situation_object_lanelets import visualize, visualize_lanelets2cover
from util_simulation.vehicle.main import Vehicle
from util_simulation.environment_model.main import EnvironmentModel
from util_simulation.map.lanelet_map_reader import lanelet_map_reader
# from prediction.visualization.prediction_animation import PredictionAnimator # for interactive mode
from prediction.visualization.plot_occupancy_prediction import plotOccupancy


class SimulationConfigurations(object):
    def __init__(self, scene, v_id, eval_ms_begin, eval_ms_end, horizon=6000, toLanelet=None):
        self.dt = 100  # ms
        self.horizon = int(horizon)
        self.N = int(self.horizon / self.dt)

        self.scene = scene
        self.v_id = v_id
        self.to_lanelet = toLanelet
        self.eval_ms_begin = eval_ms_begin
        self.eval_ms_end = eval_ms_end

        self.prediction_configurations = {
            "set_ground_truh_values": True,
            "multi_modal": False,  # True for ITSC'18 settings, False for IV'18 settings
            "politeness_factor": 0.5,
            "deceleration_comfortable": -5.0,
            "deceleration_maximum": -8.0,
            "acceleration_maximum": 2.5,
            "deceleration_comfortable_host": -3.0
        }

class BenchmarkVehicle(Vehicle):
    def __init__(self, t, to_lanelet):
        """
        Parameters
        ----------
        t: Track
            Track of benchmark vehicle
        """
        super(BenchmarkVehicle, self).__init__(t.track_id)

        self.appearance.length = t.length
        self.appearance.width = t.width
        self.timestamp_max = t.time_stamp_ms_last
        self.to_lanelet = to_lanelet

    def add_timestamp(self, timestamp):
        assert (isinstance(timestamp, int))
        self.timestamps.create_and_add(timestamp)


class PredictionSimulator(object):
    def __init__(self, config):
        self.bindings = InteractionDatasetBindings(config.scene, config.dt)
        self.vehicle_track = self.bindings._dataset_handler.track_dictionary[config.v_id]
        self.v = BenchmarkVehicle(self.vehicle_track, config.to_lanelet)

        laneletmap = lanelet_map_reader(config.scene, catkin_ws_rel_dir="../../../../INTERACTION-Dataset-DR-v1_0/maps")
        self.understanding = Understand(config.dt, config.N, laneletmap, config.v_id, toLanelet=self.v.to_lanelet)
        self.prediction = Predict(config.dt, config.N, config.scene, config.prediction_configurations)
        

    def run(self, t):
        timestampdata = self._fill(t)

        ts = time.time()
        timestampdata.scene = self.understanding(timestampdata.environment)
        timestampdata.situation = self.prediction(t, timestampdata.scene)
        print("Run time: ", time.time() - ts)
        # plotOccupancy(config.scene, situation_object)

    def label(self, t):
        timestampdata = self._fill(t)
        scene_model = self.understanding(timestampdata.environment)
        # todo: perform label extraction

    def _fill(self, t):
        self.v.timestamps.create_and_add(t)
        timestampdata = self.v.timestamps.latest()
        timestampdata.environment = self.bindings.get_environment_model(t)

        # write host vehicle track_id into environment model
        timestampdata.environment._vehicle_id = config.v_id
        motion = self.bindings.get_motion_with_current_timestamp([t], config.v_id)

        if motion is None:
            raise Exception("Motion is 'None'")
        else:
            timestampdata.motion = motion
        return timestampdata



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Prediction simulation environment.')
    parser.add_argument("-r", "--run", action="store_true", help="Run prediction simulations")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run interactive simulations")
    parser.add_argument("-l", "--label", action="store_true", help="Extract ground truth label data")
    args = parser.parse_args()

    config = SimulationConfigurations("DR_DEU_Roundabout_OF", 12, 8000, 10500, toLanelet=30022)
    simulator = PredictionSimulator(config)
    if args.run:
        for t in range(config.eval_ms_begin, config.eval_ms_end + config.dt, config.dt):
            print(colored('Timestamp: ' + str(t), 'red'))
            simulator.run(t)
    elif args.interactive:
        print "currently not supported"
        #animator = PredictionAnimator(config, 7, understanding, prediction, data_handler, laneletmap, laneletmap)
        #animator.animate_maneuver_path_options()
    elif args.label:
        for t in range(config.eval_ms_begin, config.eval_ms_end + config.dt, config.dt):
            simulator.label(t)
    else:
        print "invalid"
