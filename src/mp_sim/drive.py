from util_simulation.output.consoleprint import Print2Console
#from visualization.spatiotemporal.plot_prediction import plot_prediction
#from visualization.spatiotemporal.plot_planning import plot_planning
#from visualization.spatiotemporal.plot_velocity_position import plot_xv
import pprint
import os


def drive(vehicle, ground_truth_objects, laneletmap, configurations, timestamp_now):

    save_dir = configurations['save_dir']
    to_lanelet = configurations['toLanelet']

    Print2Console.p('s', ['-' * 72], style='cyan', bold=True, first_col_w=40)
    Print2Console.p('ss', ['Computing vehicle: ', vehicle.v_id], style='cyan', bold=True, first_col_w=40)
    Print2Console.p('s', ['-' * 72], style='cyan', bold=True, first_col_w=40)

    timestampdata = vehicle.timestamps.latest()
    Print2Console.p('s', ['\nNodes for computation: '], style='blue', bold=False, first_col_w=40)
    pprint.pprint(timestampdata.motion.cartesian.position.mean[-4:])
    curr_save_dir = os.path.join(save_dir, str(timestamp_now), str(vehicle.v_id))
    os.makedirs(curr_save_dir)

    # Localization -----------------------------------------------------------------------------------------------------
    # todo: pass gaussian distr. & use 2D-localization
    position = timestampdata.motion.frenet.position.mean[-1, 0]
    speed = timestampdata.motion.frenet.velocity.mean[-1, 0]
    localization_model = vehicle.modules.localization(position, speed)
    timestampdata.localization = localization_model

    # Perception -------------------------------------------------------------------------------------------------------
    current_cartesian_pos = timestampdata.motion.cartesian.position[-1]
    current_yaw_angle = timestampdata.motion.yaw_angle[-1]
    timestampdata.scene = vehicle.modules.perception(ground_truth_objects, current_cartesian_pos.mean, current_yaw_angle, vehicle.v_id)

    # Understanding ----------------------------------------------------------------------------------------------------
    vehicle.modules.understanding(timestampdata.scene, timestampdata.motion)

    # Understanding and Prediction -------------------------------------------------------------------------------------
    timestampdata.situation = vehicle.modules.prediction(timestampdata.scene)
    #plot_prediction(situation_model.objects, vehicle.vehicle_id, settings["Main"]["N"], settings["Main"]["dt"], curr_save_dir)

    # Decision Making --------------------------------------------------------------------------------------------------
    timestampdata.decision_base = vehicle.modules.decision(timestampdata.scene, timestampdata.situation, to_lanelet)
    #plot_planning(vehicle, current_time, lightsaber_base, settings)

    # Motion Planning --------------------------------------------------------------------------------------------------
    timestampdata.motion_plans = vehicle.modules.planner(timestampdata.decision_base, current_cartesian_pos)
    #plot_planning(vehicle, current_time, decision_base, settings)

    # Pick the optimal action ------------------------------------------------------------------------------------------
    vehicle.modules.action(timestampdata.motion_plans)

