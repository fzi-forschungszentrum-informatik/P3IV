# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

from visualization.spatiotemporal.utils.spatiotemporalPlotUtils import *


def plot_xv(vehicle, map_data, settings, current_time):
    dt, N, N_pin_past, N_pin_future, safety_dist, start_time, speed_limit = read_settings(settings)

    fig = plt.figure()
    fig.suptitle("Long. velocity vs. long. position", fontsize=14, fontweight="bold")

    ax = plt.subplot(111)
    ax.set_xlabel("Longitudinal position $(m)$")
    ax.set_ylabel("Longitudinal velocity $(m/s)$")

    # Get planned optimal motion data
    ts_data = vehicle.timestampdata[current_time]
    if ts_data.opt_tc_index is not None:
        opt_comb = ts_data.combinations.optimized[ts_data.opt_tc_index][ts_data.opt_combntn]
    else:
        opt_comb = ts_data.combinations.optimized[ts_data.opt_combntn]

    traj = opt_comb.motion.frenet.position[:, 0]
    vel = opt_comb.motion.frenet.velocity[:, 0]

    ax.plot(traj, vel, color="black", linestyle="-", alpha=0.8, linewidth=1)

    try:
        if vehicle.properties.route == "ego":
            # TODO: fix the hard coded other3
            x_line = map_data.roads[vehicle.properties.route].center.segments["other3"].l_before_coincidence
        else:
            x_line = map_data.roads[vehicle.properties.route].center.segments["ego"].l_before_coincidence
        ax.axvline(x_line, color="red", linestyle="--")
    except:
        pass

    ax.set_xlim(np.min(traj), np.max(traj))
    ax.set_ylim(np.min(vel) * 0.9, np.max(vel) * 1.1)

    # Save figure with date and time ###################################################################################

    save_dir = start_time + "/" + str(current_time) + "/" + vehicle.vehicle_id + "/"
    filename = vehicle.vehicle_id + "_position_velocity"

    save_figure(fig, save_dir, filename)

    plt.close()
