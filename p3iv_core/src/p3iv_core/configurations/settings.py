import os

ws_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../.."))
ws_path = os.path.realpath(ws_path)

settings = {
    "interaction_dataset_dir": os.path.join(ws_path, "INTERACTION-Dataset-DR-v1_0"),
    "temporal": {
        "horizon": 6,  # s
        "dt": 100,  # ms (step-width)
        "N_pin_past": 4,  # including current; so there are 3 points in the past!
        "N_pin_future": 3,
        # N is calculated automatically; int(horizon / dt)
    },
    "localization": {
        "position_sigma_longitudinal": 2,
        "position_sigma_lateral": 0.5,
        "position_cross_correlation": 0.0,
        "velocity_sigma_longitudinal": 1,
        "velocity_sigma_lateral": 0.2,
        "velocity_cross_correlation": 0.0,
    },
    "prediction": {
        "multi_modal": False,
        "politeness_factor": 0.5,
        "deceleration_comfortable": -5.0,
        "deceleration_maximum": -8.0,
        "acceleration_maximum": 2.5,
        "deceleration_comfortable_host": -3.0,
        "type": "pseudo",
    },
    "perception": {
        "perception_noise": 0.8,
        "position_sigma_longitudinal": 2,
        "position_sigma_lateral": 0.5,
        "position_cross_correlation": 0.0,
        "velocity_sigma_longitudinal": 1,
        "velocity_sigma_lateral": 0.2,
        "velocity_cross_correlation": 0.0,
        "egoVehicle_sensor_range": 40.0,
        "otherVehicle_sensor_range": 30.0,
        "egoVehicle_sensor_fov": 150,
        "otherVehicle_sensor_fov": 130,
    },
    "decision_making": {
        "pkg_name": None,
        "astar_initialization": False,
    },
    "planning": {
        "distance2static_obs": 1.0,  # m
        "v2v_safety_dist": 6.0,  # m
        "override_max_deceleration": True,
        "max_deceleration": 9.0,
        "initialization_astar": False,
        "type": "constant_velocity",
    },
}
