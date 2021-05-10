import numpy as np
import matplotlib.pyplot as plt
import os


def read_settings(settings):
    dt = settings["Main"]["dt"]
    N = settings["Main"]["N"]
    N_pin_past = settings["Opt"]["ceres1d"]["N_pin_past"]
    N_pin_future = settings["Opt"]["ceres1d"]["N_pin_future"]
    safety_dist = settings["Planning"]["v2v_safety_dist"]
    save_dir = settings["save_dir"]
    speed_limit = settings["Planning"]["speed_limit"]
    return [dt, N, N_pin_past, N_pin_future, safety_dist, save_dir, speed_limit]


def get_position_bounds_from_vehicles(l_start, l_reachable_upper, vehicles_in_path, sigma=2, delta=20.0):

    # Initialize values
    l_min = l_start - delta
    l_max = l_reachable_upper

    if vehicles_in_path is not None and len(vehicles_in_path) > 0:
        for v in vehicles_in_path:
            pred = v.prediction
            upper_bound = pred.uncertain_motion["drive"].position.get_upper_bound(sigma)
            lower_bound = pred.uncertain_motion["give_way"].position.get_lower_bound(sigma)

            l_max_ = upper_bound[-1] + delta

            if l_max_ > l_max:
                l_max = l_max_

    return l_min, l_max


def update_axis_limits(ax, l_start, l_max, l_min, N, dt):
    # Update the axis limits accordingly
    if l_start > l_max:
        l_max = l_start
    elif l_start < l_min:
        l_min = l_start
    ax.set_xlim(0, N * dt)
    ax.set_ylim(l_min * 0.9, l_max * 1.1)


def create_figure(header, ylabel="Longitudinal Position $(m)$"):
    fig = plt.figure(header)
    fig.suptitle(header, fontsize=14, fontweight="bold")
    ax = plt.subplot(111)
    ax.set_xlabel("Time $(s)$")
    ax.set_ylabel(ylabel)
    return fig, ax


def save_figure(fig, save_dir, filename):
    if os.path.isdir(save_dir) is False:
        os.makedirs(save_dir)
    fig.set_size_inches((24.0, 15.0))
    fig.savefig(save_dir + filename + ".svg", dpi=fig.dpi)


def plot_ego_motion_profile(ax, motion_profile, N, dt, color, linewidth=5, ms=3.0):
    time_range = dt * np.arange(N + 1)
    assert N + 1 == len(motion_profile)
    ax.plot(time_range, motion_profile, "o-", linewidth=linewidth, color=color, ms=ms)


def plot_desired_motion_profile(ax, N, dt, l_start, speed_des):
    desired_motion_t = np.linspace(0, N * dt, N + 1)
    desired_motion_l = [l + l_start for l in desired_motion_t * speed_des]
    ax.plot(desired_motion_t, desired_motion_l, color="r", linestyle="--", alpha=0.8, linewidth=1)


def plot_ego_motion_limits(ax, vehicle, current_time, N, dt):
    time_range = dt * np.arange(N + 1)

    upper_motion_limit = vehicle.timestampdata[current_time].executed.safety.acceler_traj
    lower_motion_limit = vehicle.timestampdata[current_time].executed.safety.braking_traj

    upper = ax.fill_between(
        time_range, upper_motion_limit + 10000, upper_motion_limit, facecolor=vehicle.properties.color, alpha=0.1
    )
    lower = ax.fill_between(
        time_range, lower_motion_limit, lower_motion_limit - 10000, facecolor=vehicle.properties.color, alpha=0.1
    )

    return [upper, lower]
