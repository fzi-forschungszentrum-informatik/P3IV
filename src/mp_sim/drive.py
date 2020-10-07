from data_types.timestamp import update_timestamp_object
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

    # timestamp object UPDATE
    """
    if len(vehicle.timestamps) > 0:
        raw_input("Warn drive.py @ mp_sim")
        vehicle.timestampdata[timestamp_now] = update_timestamp_object(timestamp_now, vehicle)
    #vehicle.timestamps.append(timestamp_now)
    """
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
    decision_base = vehicle.modules.decision(timestampdata.scene, timestampdata.situation, to_lanelet)
    #vehicle.timestampdata[timestamp_now].decision_base = decision_base
    #plot_planning(vehicle, current_time, lightsaber_base, settings)

    # Motion Planning --------------------------------------------------------------------------------------------------
    #vehicle.plan(situation_model, decision_base, timestamp_now)
    vehicle.modules.plan(timestampdata.environment, timestamp_now)
    #plot_planning(vehicle, current_time, decision_base, settings)

    # Execution --------------------------------------------------------------------------------------------------------
    vehicle.act(timestamp_now)

    """
    # dummy calculation for postprocessing
    for i, v in enumerate(ground_truth_objects):
        if "ego" not in v.vehicle_id:
            percepted_obj_id = [p.vehicle_id for p in environment_model.percepted_vehicles]
            if v.vehicle_id in percepted_obj_id:
                dist = v.timestampdata[current_time].executed.frenet.position[-1, 0] - position
            else:
                dist = None
            vehicle.timestampdata[current_time].distance2obj = dist

    plot_xv(vehicle, map_data, settings, current_time)
    """
    # Update vehicle data
    for i, v in enumerate(ground_truth_objects):
        if v.vehicle_id == vehicle.vehicle_id:
            ground_truth_objects[i] = vehicle

    return ground_truth_objects


