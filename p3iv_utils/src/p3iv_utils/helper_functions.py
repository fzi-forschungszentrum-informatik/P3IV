
import numpy as np


def get_yaw_angle(pos_data, yaw0=None):
    """
    Find the yaw angle/orientation of the vehicle
    """
    diff = np.diff(pos_data, axis=0)
    displacement = np.vstack([diff[0], diff])
    yaw = np.degrees(np.arctan2(displacement[:, 1], displacement[:, 0]))
    if yaw0 is not None:
        yaw[0] = yaw0
    # make more human-readable
    for i, y in enumerate(yaw):
        yaw[i] = (y + 360) % 360
    return np.asarray(yaw)


def get_yaw_rate(yaw_data, dt):
    rate = np.diff(yaw_data, axis=0) / dt
    yaw_rate = np.concatenate([[0], rate])
    return yaw_rate


def rotate_vector(vector, radian):
    # vector can be for example: vector = array([1, 0])

    rot_matrix = np.array([[np.cos(radian), -np.sin(radian)], [np.sin(radian), np.cos(radian)]])

    return rot_matrix.dot(vector)
