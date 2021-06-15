import warnings
from p3iv_types.vehicle import Vehicle
from p3iv_types.ground_truth import GroundTruth
from p3iv_types.environment_model import EnvironmentModel
from p3iv_modules.modules import VehicleModules
from p3iv_utils.consoleprint import Print2Console
from .track_reader import track_reader
from .data_converter import DataConverter


class InteractionDatasetBindings(object):
    def __init__(self, track_name, interaction_dataset_dir, dt):
        track_dictionary = track_reader(track_name, interaction_dataset_dir)
        self._dataset_handler = DataConverter(int(dt), track_dictionary)

    def get_environment_model(self, timestamp):
        e = EnvironmentModel()
        return self._dataset_handler.fill_environment(e, timestamp)

    def get_state(self, timestamp, object_id):
        return self._dataset_handler.get_state(timestamp, object_id)

    @staticmethod
    def spawn_simulation_object(scene_object, laneletmap, configurations):

        v = Vehicle(scene_object.id)

        if scene_object.id == configurations["vehicle_of_interest"]:
            scene_object.color = "black"

        # fill appearance
        v.appearance.color = scene_object.color
        v.appearance.length = scene_object.length
        v.appearance.width = scene_object.width

        # fill objective
        try:
            v.objective.toLanelet = configurations["planning_meta"][scene_object.id][0]
        except KeyError:
            # make sure that 'toLanelet' is defined for vehicle-of-interest
            assert v.id is not configurations["vehicle_of_interest"]
        # v.objective.set_speed = ""

        # fill perception
        if scene_object.id != configurations["vehicle_of_interest"]:
            v.perception.sensor_fov = configurations["perception"]["otherVehicle_sensor_fov"]
            v.perception.sensor_range = configurations["perception"]["otherVehicle_sensor_range"]
        else:
            v.perception.sensor_fov = configurations["perception"]["egoVehicle_sensor_fov"]
            v.perception.sensor_range = configurations["perception"]["egoVehicle_sensor_range"]
        v.perception.sensor_noise = configurations["perception"]["perception_noise"]

        # instantiate modules
        v.modules = VehicleModules(configurations, laneletmap, v)

        return v

    def create_ground_truth(self, object_list, laneletmap, configurations):
        gt = GroundTruth()

        for o in object_list:
            Print2Console.p("ss", ["Spawn new vehicle with ID: %s" % str(o.id)], style="yellow")
            Print2Console.p("s", ["-" * 72], style="yellow")

            v = self.spawn_simulation_object(o, laneletmap, configurations)
            gt.append(v)

        return gt

    def update_open_loop_simulation(self, ground_truth, timestamp, laneletmap, configurations):
        current_env_model = self.get_environment_model(timestamp)
        for o in current_env_model.objects():
            if o.id in list(ground_truth.keys()):
                self.update_simulation_object(ground_truth.get(o.id), timestamp)
            else:
                v = self.spawn_simulation_object(o, laneletmap, configurations)
                self.update_simulation_object(v, timestamp)
                ground_truth.append(v)

    def update_simulation_object(self, v, timestamp):
        """Update the values of GroundTruth-Vehicle from dataset."""
        assert isinstance(v, Vehicle)
        assert isinstance(timestamp, int)

        # try to read state data for this timestamp
        state = self.get_state(int(timestamp), v.id)

        if len(v.timestamps) == 0:
            v.timestamps.create_and_add(timestamp)
        # create a timestamp if it does not exist
        elif v.timestamps.latest().timestamp != timestamp:
            v.timestamps.create_and_add(timestamp)
        else:
            warnings.warn("Timestamp is already present in Timestamps!")

        v.timestamps.latest().state = state
