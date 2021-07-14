# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import abc
import warnings
import numpy as np
import matplotlib.pyplot as plt
from p3iv_types.vehicle import Vehicle
from p3iv_types.vehicle import VehicleSensorFOV
from p3iv_types.ground_truth import GroundTruth
from p3iv_types.environment_model import EnvironmentModel
from p3iv_types.motion import MotionState
from p3iv_modules.modules import VehicleModules
from p3iv_utils.consoleprint import Print2Console


class DataConverterInterface(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        self._tracks = None

    @property
    def tracks(self):
        return self._tracks

    @abc.abstractmethod
    def get_state(self, timestamp, object_id):
        pass

    @abc.abstractmethod
    def fill_environment(self, environment_model, timestamp):
        pass

    @staticmethod
    def state(x, y, psi_rad, vx, vy):
        """Cast current state values to MotionState."""

        state = MotionState()
        state.position.mean = np.array([x, y])
        state.yaw.mean = (np.degrees(psi_rad) + 360.0) % 360.0
        state.velocity.mean = np.array([vx, vy])
        return state

    def get_color(self, object_id):
        colormap = plt.cm.get_cmap("jet", 20)
        return colormap(object_id % 20)


class SimulationBindings(object):
    def __init__(self, configurations, laneletmap):
        self.laneletmap = laneletmap
        self.configurations = configurations

        if configurations["source"] == "interaction_sim":
            from .interaction_dataset.data_converter import DataConverter

        elif configurations["source"] == "d_sim":
            from .d_dataset.data_converter import DataConverter

        else:
            from .custom_simulation.data_converter import DataConverter

        self._data_handler = DataConverter(configurations)
        assert isinstance(self._data_handler, DataConverterInterface)

    def get_environment_model(self, timestamp):
        e = EnvironmentModel()
        return self._data_handler.fill_environment(e, timestamp)

    def create_ground_truth(self, timestamp):
        e = self.get_environment_model(timestamp)
        gt = GroundTruth()
        for o in e.objects():
            v = self._spawn_simulation_object(o)
            gt.append(v)
        return gt

    def update_open_loop_simulation(self, ground_truth, timestamp):
        current_env_model = self.get_environment_model(timestamp)
        for o in current_env_model.objects():
            if o.id in list(ground_truth.keys()):
                self._update_object(ground_truth.get(o.id), timestamp)
            else:
                v = self._spawn_simulation_object(o)
                self._update_object(v, timestamp)
                ground_truth.append(v)

    def _spawn_simulation_object(self, scene_object):
        Print2Console.p("ss", ["Spawn new vehicle with ID: %s" % str(scene_object.id)], style="yellow")
        Print2Console.p("s", ["-" * 72], style="yellow")

        v = Vehicle(scene_object.id)

        if scene_object.id == self.configurations["vehicle_of_interest"]:
            scene_object.color = "black"

        # fill appearance
        v.appearance.color = scene_object.color
        v.appearance.length = scene_object.length
        v.appearance.width = scene_object.width

        # fill objective
        try:
            v.objective.toLanelet = self.configurations["meta_state"][scene_object.id][0]
        except KeyError:
            # make sure that 'toLanelet' is defined for vehicle-of-interest
            assert v.id is not self.configurations["vehicle_of_interest"]
        # v.objective.set_speed = ""

        # fill sensors
        sensors = []
        if scene_object.id != self.configurations["vehicle_of_interest"]:
            for sensor in self.configurations["perception"]["otherVehicle_sensors"]:
                sensors.append(VehicleSensorFOV(*sensor))
        else:
            for sensor in self.configurations["perception"]["egoVehicle_sensors"]:
                sensors.append(VehicleSensorFOV(*sensor))
        v.perception.sensors = sensors

        # instantiate modules
        v.modules = VehicleModules(self.configurations, self.laneletmap, v)

        return v

    def _update_object(self, v, timestamp):
        """Update the values of GroundTruth-Vehicle using dataset."""
        assert isinstance(v, Vehicle)
        assert isinstance(timestamp, int)

        # try to read state data for this timestamp
        state = self._data_handler.get_state(int(timestamp), v.id)

        if len(v.timestamps) == 0:
            v.timestamps.create_and_add(timestamp)
        # create a timestamp if it does not exist
        elif v.timestamps.latest().timestamp != timestamp:
            v.timestamps.create_and_add(timestamp)
        else:
            warnings.warn("Timestamp is already present in Timestamps!")

        v.timestamps.latest().state = state
