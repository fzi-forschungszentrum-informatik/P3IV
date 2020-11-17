import warnings
import numpy as np
from util_simulation.vehicle.main import Vehicle
from util_simulation.ground_truth.main import GroundTruth
from util_simulation.output.consoleprint import Print2Console
from mp_sim.modules import VehicleModules
from understanding.lanelet_sequence_analyzer import LaneletSequenceAnalyzer
from interpolated_distance.coordinate_transformation import CoordinateTransform
from interaction_prediction_sim.interaction_data_extractor import track_reader
from interaction_prediction_sim.interaction_data_handler import InteractionDataHandler


class InteractionDatasetBindings(object):
    def __init__(self, instance_settings, laneletmap):
        track_dictionary = track_reader(instance_settings["map"])
        self.data_handler = InteractionDataHandler(int(instance_settings["temporal"]["dt"]), track_dictionary)
        self.lanelet_sequence_analyzer = LaneletSequenceAnalyzer(laneletmap)

    def get_scene_model(self, timestamp):
        return self.data_handler.fill_scene(timestamp)

    def spawn_simulation_object(self, scene_object, laneletmap, configurations):

        v = Vehicle(scene_object.v_id)

        # fill appearance
        v.appearance.color = scene_object.color
        v.appearance.length = scene_object.length
        v.appearance.width = scene_object.width

        # fill objective
        try:
            v.objective.toLanelet = configurations['toLanelet'][scene_object.v_id]
        except KeyError:
            # make sure that 'toLanelet' is defined for vehicle-of-interest
            assert v.v_id is not configurations['vehicle_of_interest']
        # v.objective.set_speed = ""

        # fill perception
        if scene_object.v_id != configurations['vehicle_of_interest']:
            v.perception.sensor_fov = configurations['perception']['otherVehicle_sensor_fov']
            v.perception.sensor_range = configurations['perception']['otherVehicle_sensor_range']
        else:
            v.perception.sensor_fov = configurations['perception']['egoVehicle_sensor_fov']
            v.perception.sensor_range = configurations['perception']['egoVehicle_sensor_range']
        v.perception.sensor_noise = configurations['perception']['perception_noise']

        # instantiate modules
        v.modules = VehicleModules(configurations, laneletmap, v)

        return v

    def create_ground_truth(self, object_list, laneletmap, configurations):
        gt = GroundTruth()

        for o in object_list:
            Print2Console.p('ss', ['Create new vehicle with ID: %s' % str(o.v_id)], style='yellow')
            Print2Console.p('s', ['-'*72], style='yellow')

            v = self.spawn_simulation_object(o, laneletmap, configurations)
            gt.append(v)

        return gt

    def update_open_loop_simulation(self, ground_truth, timestamp, laneletmap, configurations):

        current_scene_model = self.get_scene_model(timestamp)
        for o in current_scene_model.tracked_objects():
            if o.v_id in ground_truth.keys():
                self.update_simulation_object_motion(ground_truth.get(o.v_id), timestamp)
            else:
                v = self.spawn_simulation_object(o, laneletmap, configurations)
                self.update_simulation_object_motion(v, timestamp)
                ground_truth.append(v)

    def update_simulation_object_motion(self, v, timestamp):
        """Update the values of GroundTruth-Vehicle from dataset.
        """
        assert (isinstance(v, Vehicle))
        assert (isinstance(timestamp, int))

        if len(v.timestamps) == 0:
            v.timestamps.create_and_add(timestamp)
        # create a timestamp if it does not exist
        elif v.timestamps.latest().timestamp != timestamp:
            v.timestamps.create_and_add(timestamp)
        else:
            warnings.warn("Timestamp is already present in Timestamps!")

        motion = self.data_handler.update_scene_object_motion(timestamp, v.v_id)
        v.timestamps.latest().motion = self._fill_frenet_motion(motion, v.objective.toLanelet)

    def _fill_frenet_motion(self, motion, toLanelet):
        if toLanelet:
            lanelet_path_wrapper = self.lanelet_sequence_analyzer.lanelets2destination(motion, toLanelet)
        else:
            # we do not know 'toLanelet', i.e. where vehicles are heading; may cause problems if centerline is
            # short for Frenet->Cartesian transformation.
            lanelet_path_wrapper = self.lanelet_sequence_analyzer.match(motion)
        centerline = lanelet_path_wrapper.centerline()
        c = CoordinateTransform(centerline)
        pos_frenet = c.xy2ld(motion.cartesian.position.mean[-4:])
        motion.frenet(pos_frenet, dt=0.1)
        return motion
