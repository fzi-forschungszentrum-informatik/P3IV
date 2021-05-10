from __future__ import division
from p3iv_visualization.spatiotemporal.utils.spatiotemporalPlotUtils import *
from p3iv_visualization.spatiotemporal.utils.plot_utils import PlotUtils
from p3iv_visualization.spatiotemporal.utils.plot_ego_motion import PlotEgoMotion
from p3iv_visualization.spatiotemporal.utils.plot_other_vehicles import PlotOtherVehicles


def plot_combination(vehicle, current_time, vehicle_colors, combination, settings, show=False):
    dt, N, N_pin_past, N_pin_future, _, start_time, speed_limit = read_settings(settings)

    # Get important values
    header = vehicle.vehicle_id + "_combination_" + combination.combination_id
    if combination.motion:
        header += "_profile"

    output_dir = (
        start_time + "/" + str(current_time) + "/" + vehicle.vehicle_id + "/" + combination.combination_id + "/"
    )

    # Plot
    p = PlotUtils()
    p.create_figure(header)
    p.set_settings(dt, N, output_dir)

    pov = PlotOtherVehicles(p.ax, p.dt)
    pov.plot_objects(combination, vehicle_colors)

    if combination.motion is not None:
        motion_profile = combination.motion[N_pin_past - 1 :]
        pem = PlotEgoMotion(p.ax, vehicle.vehicle_id, vehicle.properties.color)
        pem.create_motion_profile(p.dt, p.N)
        pem.update_motion_profile(motion_profile)
        pem.create_stop_positions()
        pem.update_stop_positions(motion_profile, N_pin_past + 2 * N_pin_future)
        pem.create_initial_position()
        pem.update_initial_position(motion_profile)

    p.set_labels()

    if show:
        plt.show()
    else:
        p.save_figure()
        plt.close()


def plot_planning(vehicle, current_time, combinatorial_alternatives, settings):
    for combination in combinatorial_alternatives.combinations.values():
        plot_combination(vehicle, current_time, combinatorial_alternatives.vehicle_colors, combination, settings)
