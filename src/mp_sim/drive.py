from util_simulation.output.consoleprint import Print2Console
import pprint


def drive(vehicle, ground_truth):

    Print2Console.p('s', ['-' * 72], style='cyan', bold=True, first_col_w=40)
    Print2Console.p('ss', ['Computing vehicle: ', vehicle.v_id], style='cyan', bold=True, first_col_w=40)
    Print2Console.p('s', ['-' * 72], style='cyan', bold=True, first_col_w=40)

    timestampdata = vehicle.timestamps.latest()
    Print2Console.p('s', ['\nNodes for computation: '], style='blue', bold=False, first_col_w=40)
    pprint.pprint(timestampdata.motion.cartesian.position.mean[-4:])

    # Localization -----------------------------------------------------------------------------------------------------
    # todo: pass gaussian distr. & use 2D-localization
    position = timestampdata.motion.frenet.position.mean[-1, 0]
    speed = timestampdata.motion.frenet.velocity.mean[-1, 0]
    localization_model = vehicle.modules.localization(position, speed)
    timestampdata.localization = localization_model

    # Perception -------------------------------------------------------------------------------------------------------
    current_cartesian_pos = timestampdata.motion.cartesian.position.mean[-1]
    current_yaw_angle = timestampdata.motion.yaw_angle[-1]
    timestampdata.scene = vehicle.modules.perception(ground_truth, current_cartesian_pos, current_yaw_angle, vehicle.v_id)

    # Understanding ----------------------------------------------------------------------------------------------------
    vehicle.modules.understanding(timestampdata.scene, timestampdata.motion)

    # Understanding and Prediction -------------------------------------------------------------------------------------
    timestampdata.situation = vehicle.modules.prediction(timestampdata.scene)

    # Decision Making --------------------------------------------------------------------------------------------------
    timestampdata.decision_base = vehicle.modules.decision(timestampdata.scene, timestampdata.situation, vehicle.objective.toLanelet)

    # Motion Planning --------------------------------------------------------------------------------------------------
    timestampdata.decision_base.past4points = timestampdata.motion.frenet.position.mean[-4:, 0]
    timestampdata.decision_base.current_spd = timestampdata.motion.frenet.velocity.mean[-1, 0]
    timestampdata.motion_plans = vehicle.modules.planner(timestampdata.decision_base, current_cartesian_pos)

    # Pick the optimal action ------------------------------------------------------------------------------------------
    vehicle.modules.action(timestampdata.motion_plans)

