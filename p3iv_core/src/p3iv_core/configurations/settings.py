import os

ws_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../.."))
ws_path = os.path.realpath(ws_path)

settings = {
    "interaction_dataset_dir": os.path.join(ws_path, "INTERACTION-Dataset-DR-v1_0"),
    "main": {
        "travel_length": 0.2,  # defined in seconds
        "combinatorial_greedy_search": True,
        # False for IV'18 settings, True for ITSC'18 settings (note that this has an effect on initialization!)
        # True for IV'18 settings, False for ITSC'18 settings
        "provably_safe_planning": False,
    },
    "temporal": {
        "horizon": 6,  # s
        "dt": 100,  # ms (step-width)
        "N_pin_past": 4,  # including current; so there are 3 points in the past!
        "N_pin_future": 3,
        # N is calculated automatically; int(horizon / dt)
    },
    "localization": {
        "measurement_noise": 1.2,
        "process_noise": 0.5,
    },
    "prediction": {
        "set_ground_truh_values": False,
        "multi_modal": False,  # True for ITSC'18 settings, False for IV'18 settings
        "politeness_factor": 0.5,
        "deceleration_comfortable": -5.0,
        "deceleration_maximum": -8.0,
        "acceleration_maximum": 2.5,
        "deceleration_comfortable_host": -3.0,
    },
    "perception": {
        "perception_noise": 0.8,
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
        # use the value specified here instead of the OSM file
        "override_max_deceleration": True,
        "max_deceleration": 9.0,
        "initialization_astar": False,
        "type": "constant_velocity",
    },
}
