from __future__ import division
import numpy as np


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
