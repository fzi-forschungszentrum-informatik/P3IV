import numpy as np
from scipy.interpolate import UnivariateSpline


def smooth(x_data, y_data, order=5, resolution=None):
    if resolution:
        x_data_req = np.linspace(x_data[0], x_data[-1], resolution)
    else:
        x_data_req = x_data

    try:
        spline = UnivariateSpline(x_data, y_data, k=order)
        spline.set_smoothing_factor(1.0)
        y_data = spline(x_data_req)
        return y_data
    except:
        # if the input array too short, scipy will raise dfitpack.error
        return y_data


def get_yaw_angle(pos_data, yaw0=None):
    """
    Find the yaw angle/orientation of the vehicle using finite differences.

    Finite differences amplify numerical erros considerably. Ttherefore,
    we perform spline interpolation and smooth yaw angle profile.
    """
    diff = np.diff(pos_data, axis=0)
    displacement = np.vstack([diff[0], diff])

    # calculate yaw angle using finite differences; in some cases finite differences cause numerical erros
    # therefore, we perform spline interpolation and smooth yaw angle profile.
    yaw = np.degrees(
        np.arctan2(
            smooth(range(len(displacement[:, 1])), displacement[:, 1]),
            smooth(range(len(displacement[:, 0])), displacement[:, 0]),
        )
    )
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


def unit_vector(vector):
    """
    Returns the unit vector of the vector
    """
    return vector / np.linalg.norm(vector)


def angle_between_vectors(v1, v2):
    """
    Returns the angle in radians between vectors 'v1' and 'v2'
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
