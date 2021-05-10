import numpy as np
import random
from matplotlib import colors as mcolors
from timestamp import Timestamps


def get_color(index):
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    return colors.keys()[index]


class VehicleAppearance(object):

    __slots__ = ["_color", "_length", "_width"]

    def __init__(self):
        super(VehicleAppearance, self).__init__()

        self._color = get_color(random.randint(0, 155))
        self._length = 0.0
        self._width = 0.0

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        assert isinstance(color, (unicode, str))
        self._color = color

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


class VehicleRectangle(object):

    __slots__ = []

    @classmethod
    def get_corners(cls, length, width, xy, theta):
        # create corner points ignoring the yaw angle of the percepted vehicle
        left_rear_pre = np.array([xy[0] - width / 2, xy[1] - length / 2])
        right_rear_pre = np.array([xy[0] + width / 2, xy[1] - length / 2])
        left_front_pre = np.array([xy[0] - width / 2, xy[1] + length / 2])
        right_front_pre = np.array([xy[0] + width / 2, xy[1] + length / 2])

        # rotate vehicle corner points according to yaw angle
        left_rear = cls.rotate(left_rear_pre, xy, theta)
        right_rear = cls.rotate(right_rear_pre, xy, theta)
        left_front = cls.rotate(left_front_pre, xy, theta)
        right_front = cls.rotate(right_front_pre, xy, theta)

        return np.asarray([left_rear, left_front, right_front, right_rear])

    @staticmethod
    def rotate(point, origin, angle):  # rotates point around origin
        ox, oy = origin
        px, py = point

        angle_rad = np.deg2rad(angle)
        qx = ox + np.cos(angle_rad) * (px - ox) - np.sin(angle_rad) * (py - oy)
        qy = oy + np.sin(angle_rad) * (px - ox) + np.cos(angle_rad) * (py - oy)
        rotated_point = np.array([qx, qy])
        return rotated_point


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
