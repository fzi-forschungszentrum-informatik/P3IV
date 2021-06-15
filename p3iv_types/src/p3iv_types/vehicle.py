import numpy as np
import itertools
from .timestamp import Timestamps
from .tracked_object import TrackedObject, ExistenceProbability


class VehicleAppearanceBase:
    __slots__ = ["_length", "_width"]


class VehicleAppearance(object, VehicleAppearanceBase):
    __slots__ = []

    def __init__(self):
        super(VehicleAppearance, self).__init__()
        self._length = 0.0
        self._width = 0.0

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


class VehiclePerception(object):

    __slots__ = ["sensor_range", "sensor_fov", "sensor_noise"]

    def __init__(self, sensor_range=50, sensor_fov=120, sensor_noise=0.8):
        super(VehiclePerception, self).__init__()
        self.sensor_range = sensor_range  # in meters
        self.sensor_fov = sensor_fov  # in degrees
        self.sensor_noise = sensor_noise  # in degrees


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


class TrackedVehicle(TrackedObject, VehicleAppearance):
    """
    Contains information on a detected vehicle.

    Attributes
    ---------
    _object_id : int
        Object id
    _color : str
        Object color
    """

    __slots__ = []

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
