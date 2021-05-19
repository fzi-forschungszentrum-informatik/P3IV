from __future__ import division
import numpy as np


def get_braking_dist(v_curr, acceleration, **kwargs):
    """
    Finite differencing position may cause wrong calculations of stop points,
    as this assumes constant acceleration in speed calculation.
    Big jerk values may significantly deviate acceleration values,
    leading to imprecise position calculations. A way to handle this is to
    abandon Newton's energy equations and reflect the discretization to the stop
    position calculation. Another approach is to use second order finite differences.
    # t_stop = v - a * dt - 0.5 * j * dt**2 (if t_stop < dt!)
    dist = v_curr * dt - 0.5 * acceleration * dt**2 - 1/6 * jerk * dt**3
    """

    return np.abs(v_curr ** 2 / (2 * acceleration))


def accelerating_motion(v_curr, acceleration, **kwargs):
    delta_time = kwargs["delta_time"]
    return v_curr * delta_time + 0.5 * acceleration * delta_time ** 2


def get_max_acc_displacements(vel_array, motion_func, acc, dt):

    N = len(vel_array)

    l_displ = np.asarray([])
    for i in range(N):
        v_curr = vel_array[max(1, i)]
        l_diff = motion_func(v_curr, acc, delta_time=(N - i) * dt)
        l_displ = np.append(l_displ, l_diff)

    return l_displ


def get_global_positions(pos_global_array, pos_displ_array):
    assert len(pos_global_array) == len(pos_displ_array)
    return np.asarray(pos_global_array) + np.asarray(pos_displ_array)


def get_max_acc_positions(pos_global_array, vel_array, motion_func, acc, dt):
    l_displ = get_max_acc_displacements(vel_array, motion_func, acc, dt)
    return get_global_positions(pos_global_array, l_displ)


def saturation(param, threshold):
    if param > threshold:
        return param
    else:
        return threshold


def get_delta_l(v, a, dt):
    delta_l = v * dt + 0.5 * a * dt ** 2
    if delta_l > 0:
        return delta_l
    else:
        t_stop = np.abs(v / a)
        return v * t_stop + 0.5 * a * t_stop ** 2


def get_delta_v(v, a, dt):
    delta_v = v + a * dt
    return saturation(delta_v, 0)


def get_max_trajectory(l_curr, v_curr, acceleration, dt, n_begin=0, n_end=0, upsampling_factor=10):
    """
    returns max braking deceleration bound for a given trajectory point
    """
    dt = dt / upsampling_factor
    n_end = n_end * upsampling_factor

    # the returned trajectory includes current position and the trajectory support points in the future
    pos = np.ones(n_end) * l_curr
    spd = np.ones(n_end) * v_curr

    for k in range(1 + n_begin * upsampling_factor, n_end):  # 1+n_begin: the first value is already set
        delta_l = get_delta_l(v_curr, acceleration, dt)
        l_curr += delta_l
        pos[k] = l_curr

        # get the speed for the next time step
        v_curr = get_delta_v(v_curr, acceleration, dt)
        spd[k] = v_curr

    pos = pos[::upsampling_factor]
    spd = spd[::upsampling_factor]

    return pos, spd


def get_max_trajectories(pos_frenet_array_plan, vel_frenet_array_plan, acceleration, dt, n_end=None):

    n_total = len(pos_frenet_array_plan)
    assert n_total == len(vel_frenet_array_plan)

    max_trajectories = np.empty((n_total, n_end))

    for i in range(n_total):
        l_curr = pos_frenet_array_plan[i]
        v_curr = vel_frenet_array_plan[i]

        max_trajectories[i], _ = get_max_trajectory(l_curr, v_curr, acceleration, dt, n_begin=i, n_end=n_end)

    return max_trajectories
