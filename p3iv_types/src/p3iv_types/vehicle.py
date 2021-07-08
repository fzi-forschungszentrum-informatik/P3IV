# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import abc
import numpy as np
import itertools
import random
from p3iv_types.timestamp import Timestamps
from .tracked_object import TrackedObject, ExistenceProbability
import matplotlib.pyplot as plt

# todo: Appereance.color is set from outside; consider deleting this
colormap = plt.cm.get_cmap("jet", 20)


class AbstractVehicleAppearance(object):
    __metaclass__ = abc.ABCMeta

    """
    Define an abstract VehicleAppearance class for mro of TrackedVehicle.
    """

    __slots__ = []

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        assert isinstance(length, (int, float))
        self._length = length

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        assert isinstance(width, (int, float))
        self._width = width

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        # assert isinstance(color, str) # comment out for Python2 compat.
        self._color = color


class VehicleAppearance(AbstractVehicleAppearance):
    __slots__ = ["_length", "_width", "_color"]

    def __init__(self):
        super(VehicleAppearance, self).__init__()
        self._length = 0.0
        self._width = 0.0
        # self._color = get_color(random.randint(0, 155))
        self._color = colormap(random.randint(0, 20))


class VehicleCharacteristics(object):

    __slots__ = ["max_acceleration", "max_deceleration"]

    def __init__(self, max_acceleration=2.0, max_deceleration=-9.81):
        super(VehicleCharacteristics, self).__init__()
        self.max_acceleration = max_acceleration
        self.max_deceleration = max_deceleration  # a negative value, although deceleration!


class VehicleObjective(object):

    __slots__ = ["_to_lanelet", "set_speed"]

    def __init__(self, set_speed=13.89):
        super(VehicleObjective, self).__init__()
        self._to_lanelet = None
        self.set_speed = set_speed

    @property
    def toLanelet(self):
        return self._to_lanelet

    @toLanelet.setter
    def toLanelet(self, to_lanelet_id):
        self._to_lanelet = int(to_lanelet_id)


class VehicleSensorFOV(object):

    __slots__ = ["begin", "end", "range", "noise"]

    def __init__(self, fov_begin, fov_end, fov_range, sensor_noise=0.8):
        """
        Field-of-view (FOV) begin and end relative to 90degrees
        """
        super(VehicleSensorFOV, self).__init__()
        self.begin = fov_begin  # in degrees
        self.end = fov_end  # in degrees
        self.range = fov_range  # in meters
        self.noise = sensor_noise


class VehiclePerception(object):

    __slots__ = ["sensors"]

    def __init__(self, sensors=[]):
        super(VehiclePerception, self).__init__()
        self.sensors = sensors  # list


class Vehicle(object):

    __slots__ = [
        "modules",
        "_object_id",
        "timestamps",
        "appearance",
        "characteristics",
        "objective",
        "perception",
        "_planner_type",
    ]

    def __init__(self, object_id):
        super(Vehicle, self).__init__()
        self._object_id = object_id

        self.timestamps = Timestamps()
        self.appearance = VehicleAppearance()
        self.characteristics = VehicleCharacteristics()
        self.objective = VehicleObjective()
        self.perception = VehiclePerception()

    @property
    def id(self):
        return self._object_id

    @id.setter
    def id(self, object_id):
        assert isinstance(object_id, (int, str))
        self._object_id = object_id


class TrackedVehicle(AbstractVehicleAppearance, TrackedObject):
    """
    Contains information on a detected vehicle.

    Attributes
    ---------
    _object_id : int
        Object id
    _color : str
        Object color
    """

    __slots__ = ["_length", "_width", "state"]

    def __init__(self):
        super(TrackedVehicle, self).__init__()

    def __setattr__(self, name, value):
        # modify setattr for multiple inheritence

        # get all slots
        all_slots = list(itertools.chain.from_iterable(getattr(t, "__slots__", ()) for t in type(self).__mro__))

        # cast slots iterable to list
        if name in all_slots:
            object.__setattr__(self, name, value)
        else:
            # call property if name is not in slots
            super(TrackedVehicle, self).__setattr__(name, value)
