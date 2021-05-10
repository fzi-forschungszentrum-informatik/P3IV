from p3iv_visualization.spatiotemporal.utils.spatiotemporalPlotUtils import *


def plot_timeshift_planning(vehicle, vehicles, maneuver_variants, settings, current_time, **kwargs):

    # Extract the required data form settings ##########################################################################
    dt, N, N_pin_past, N_pin_future, safety_dist, start_time, speed_limit = read_settings(settings)
    index_tc = kwargs["index_tc"] - 3

    # Plot the figure ##################################################################################################
    header_ = "Timeshift planner"
    filename = "timeshift_planning_" + str(index_tc)
    if "init" in kwargs["plot_type"]:
        header = header_ + " initialization"
        filename += "_initialization"
        motion_profile_0 = maneuver_variants["0"].guess[3:]
        motion_profile_1 = maneuver_variants["1"].guess[3:]

    else:
        header = header_ + " optimization"
        filename += "_optimization"
        motion_profile_0 = maneuver_variants["0"].parameters[3:]
        motion_profile_1 = maneuver_variants["1"].parameters[3:]

    fig, ax = create_figure(header)

    if kwargs["intersection_point"]:
        ax.axhline(kwargs["intersection_point"], color="red")

    # Get important values #############################################################################################
    l_start = vehicle.timestampdata[current_time].executed.frenet.position[-1, 0]
    v_start = vehicle.timestampdata[current_time].executed.frenet.velocity[-1, 0]
    l_reachable_upper = l_start + v_start * N * dt + 0.5 * vehicle.properties.max_acceleration * (N * dt) ** 2

    # Plot other vehicles ##############################################################################################
    plot_other_vehicles(ax, vehicles, dt, N, hatched=False)

    # Plot the motion limits ###########################################################################################
    plot_ego_motion_limits(ax, vehicle, current_time, N, dt)

    # Plot hard bounds #################################################################################################
    color_0 = "#a50026"
    color_1 = "#00441b"
    ax.plot(dt * np.arange(N + 1), kwargs["lower_bound0"][3:], "--", label="lower 0", color=color_0, linewidth=1.2)
    ax.plot(dt * np.arange(N + 1), kwargs["lower_bound1"][3:], "--", label="lower 1", color=color_1, linewidth=1.2)
    ax.plot(dt * np.arange(N + 1), kwargs["upper_bound0"][3:], "--", label="upper 0", color=color_0, linewidth=1.2)
    ax.plot(dt * np.arange(N + 1), kwargs["upper_bound1"][3:], "--", label="upper 1", color=color_1, linewidth=1.2)

    # Plot timeshift point #############################################################################################
    ax.plot(index_tc * dt, motion_profile_0[index_tc], "*", ms=20.0, color="red")

    # Plot motion profile of the ego vehicle ###########################################################################
    plot_ego_motion_profile(ax, motion_profile_0, N, dt, color_0, linewidth=3.0, ms=5.0)
    plot_ego_motion_profile(ax, motion_profile_1, N, dt, color_1, linewidth=3.0, ms=5.0)

    # Set the details of the figure ####################################################################################
    l_min, l_max = get_position_bounds_from_vehicles(l_start, l_reachable_upper, vehicles)
    update_axis_limits(ax, l_start, l_max, l_min, N, dt)

    # Save figure with date and time ###################################################################################
    save_dir = start_time + "/" + str(current_time) + "/" + vehicle.vehicle_id + "/"

    save_figure(fig, save_dir, filename)
    # plt.show()
    plt.close()
