import warnings
from util_simulation.vehicle.main import Vehicle
from util_simulation.ground_truth.main import GroundTruth
from mp_sim.modules import VehicleModules
from understanding.lanelet_sequence_analyzer import LaneletSequenceAnalyzer
from interpolated_distance.coordinate_transformation import CoordinateTransform
from interaction_prediction_sim.interaction_data_extractor import track_reader
from interaction_prediction_sim.interaction_data_handler import InteractionDataHandler


class InteractionDatasetBindings(object):
    def __init__(self, instance_settings, laneletmap):
        track_dictionary = track_reader(instance_settings["map"])
        self.data_handler = InteractionDataHandler(int(instance_settings["temporal"]["dt"]*1000), track_dictionary)
        self.lanelet_sequence_analyzer = LaneletSequenceAnalyzer(laneletmap)

    def get_scene_model(self, timestamp):
        return self.data_handler.fill_scene(timestamp)

    def create_simulation_objects(self, object_list, laneletmap, configurations):

        gt = GroundTruth()

        for o in object_list:
            v = Vehicle(o.v_id)
            v.appearance.color = o.color
            v.appearance.length = o.length
            v.appearance.width = o.width

            # v.objective.route = ""
            # v.objective.set_speed = ""

            if o.v_id != configurations['vehicle_of_interest']:
                v.perception.sensor_fov = configurations['perception']['otherVehicle_sensor_fov']
                v.perception.sensor_range = configurations['perception']['otherVehicle_sensor_range']
            else:
                v.perception.sensor_fov = configurations['perception']['egoVehicle_sensor_fov']
                v.perception.sensor_range = configurations['perception']['egoVehicle_sensor_range']
            v.perception.sensor_noise = configurations['perception']['perception_noise']

            v.modules = VehicleModules(configurations, laneletmap, v)

            # fill initial values of KF
            motion = self._extract_frenet_motion(o.motion)
            v.modules.localization.setup_localization(motion.frenet.position.mean[-1, 0], o.speed, 0.0)

            if o.v_id != configurations['vehicle_of_interest']:
                gt.append(v)
            else:
                voi = v
        gt.append(voi)

        return gt

    def update_simulation_objects_motion(self, ground_truth, timestamp):

        assert (isinstance(timestamp, int))
        for o in ground_truth.vehicles():

            if len(o.timestamps) == 0:
                o.timestamps.create_and_add(timestamp)
            # create a timestamp if it does not exist
            elif o.timestamps.latest().timestamp != timestamp:
                o.timestamps.create_and_add(timestamp)
            else:
                warnings.warn("Timestamp is already present in Timestamps!")

            motion = self.data_handler.update_scene_object_motion(timestamp, o.v_id)
            o.timestamps.latest().motion = self._extract_frenet_motion(motion)

        return ground_truth

    def _extract_frenet_motion(self, motion):
        lanelet_path_wrapper = self.lanelet_sequence_analyzer.match(motion)
        centerline = lanelet_path_wrapper.centerline()
        c = CoordinateTransform(centerline)
        pos_frenet = c.xy2ld(motion.cartesian.position.mean)
        motion.frenet(pos_frenet, dt=0.1)
        return motion
