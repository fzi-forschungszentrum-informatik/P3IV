from util_simulation.output.consoleprint import Print2Console
import pprint

# configure logging of the module
import os
import logging
logger = logging.getLogger(__file__.split(os.path.sep)[-2])
logger.setLevel(logging.INFO)


def drive(vehicle, ground_truth):

    Print2Console.p('s', ['-' * 72], style='cyan', bold=True, first_col_w=40)
    Print2Console.p('ss', ['Computing vehicle: ', vehicle.v_id],
                    style='cyan', bold=True, first_col_w=40)
    Print2Console.p('s', ['-' * 72], style='cyan', bold=True, first_col_w=40)

    # get the current timestampdata
    timestampdata = vehicle.timestamps.latest()

    logger.debug('Nodes for computation: ')
    logger.debug(timestampdata.motion.cartesian.position.mean[-4:])

    # Localization ------------------------------------------------------------
    timestampdata.localization = vehicle.modules.localization(
        timestampdata.motion.cartesian)

    # Perception --------------------------------------------------------------
    timestampdata.environment = vehicle.modules.perception(
        ground_truth, timestampdata.motion.pose[-1])

    # Understanding -----------------------------------------------------------
    timestampdata.scene = vehicle.modules.understanding(
        timestampdata.environment, timestampdata.motion)

    # Prediction--- -----------------------------------------------------------
    timestampdata.situation = vehicle.modules.prediction(timestampdata.timestamp, timestampdata.scene)

    # Decision Making ---------------------------------------------------------
    timestampdata.decision_base = vehicle.modules.decision(
        timestampdata.motion, timestampdata.scene, timestampdata.situation)

    # Motion Planning ---------------------------------------------------------
    timestampdata.motion_plans = vehicle.modules.planner(
        timestampdata.motion, timestampdata.scene, timestampdata.situation,
        timestampdata.decision_base)

    # Pick the optimal action -------------------------------------------------
    timestampdata.plan_optimal = vehicle.modules.action(
        timestampdata.motion, timestampdata.motion_plans)
