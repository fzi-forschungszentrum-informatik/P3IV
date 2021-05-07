from p3iv_utils.consoleprint import Print2Console
import pprint

# configure logging of the module
import os
import logging

logger = logging.getLogger(__file__.split(os.path.sep)[-2])
logger.setLevel(logging.INFO)


def drive(vehicle, ground_truth):

    Print2Console.p("s", ["-" * 72], style="cyan", bold=True, first_col_w=40)
    Print2Console.p("ss", ["Computing vehicle: ", vehicle.v_id], style="cyan", bold=True, first_col_w=40)
    Print2Console.p("s", ["-" * 72], style="cyan", bold=True, first_col_w=40)

    # get the current timestampdata
    tsd = vehicle.timestamps.latest()

    logger.debug("Nodes for computation: ")
    logger.debug(tsd.state.position.mean)

    # Localization
    tsd.localization = vehicle.modules.localization(tsd.state)

    # Perception
    tsd.environment = vehicle.modules.perception(tsd.timestamp, ground_truth, tsd.state.pose)

    # Understanding
    tsd.scene = vehicle.modules.understanding(
        tsd.environment.objects(relative_to=None), tsd.environment.polyvision, tsd.environment.visible_areas
    )

    # Prediction
    tsd.situation = vehicle.modules.prediction(tsd.timestamp, tsd.scene)

    # Decision Making
    tsd.decision_base = vehicle.modules.decision(tsd.state, tsd.scene, tsd.situation)

    # Motion Planning
    tsd.motion_plans = vehicle.modules.planner(tsd.timestamp, tsd.state, tsd.scene, tsd.situation, tsd.decision_base)

    # Pick the optimal action
    tsd.plan_optimal = vehicle.modules.action(tsd.state, tsd.motion_plans)


def predict(vehicle, ground_truth):

    # get the current timestampdata
    tsd = vehicle.timestamps.latest()

    # Perception
    tsd.environment = vehicle.modules.perception(tsd.timestamp, ground_truth, tsd.motion.pose[-1])

    # Understanding
    tsd.scene = vehicle.modules.understanding(
        tsd.environment.objects(relative_to=None), tsd.environment.polyvision, tsd.environment.visible_areas
    )

    # Prediction
    tsd.situation = vehicle.modules.prediction(tsd.timestamp, tsd.scene)
