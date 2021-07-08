# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np


def get_control_inputs(yaw_angle, speed, wheelbase, dt):
    """
    Kinematic vehicle model
    http://planning.cs.uiuc.edu/node658.html
    """

    acc = np.diff(speed) * (1.0 / dt)
    acc = np.append(acc, acc[-1])

    yaw_r = np.deg2rad(np.diff(yaw_angle) / dt)[1:]
    steering_angle = np.rad2deg(np.arctan((yaw_r * wheelbase) / speed[2:]))
    steering_angle = np.append(steering_angle, steering_angle[-1])
    # todo: TAKE CARE OF THIS APPROXIMATION HERE: INDICES!
    steering_angle = np.append(steering_angle, steering_angle[-1])
    controls = np.empty([len(acc), 2])
    controls[:, 0] = steering_angle
    controls[:, 1] = acc
    return controls
