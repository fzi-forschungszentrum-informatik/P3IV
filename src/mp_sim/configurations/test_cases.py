test_cases = {

    "DEU_Merging_CL_01": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Merging_MT',
        "timestamp_begin": 4500,
        "timestamp_end": 4500,
        "vehicle_of_interest": 1,
        "simulation_type": "closed-loop",
        # closed-loop planning is performed only for vehicles that are defined here
        # dict keys are vehicle ids, and values are 'toLanelet' and 'planner_types'
        # default reads the type from 'settings.py' file
        "planning_meta": dict([(1, ("30008", "default")),
                               (2, ("30008", "constant-velocity")),
                               (3, ("30008", "constant-velocity"))])
    },
    "DEU_Merging_OL_01": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Merging_MT',
        "timestamp_begin": 4500,
        "timestamp_end": 4500,
        "vehicle_of_interest": 1,
        "simulation_type": "open-loop",
        "planning_meta": dict([(1, ("30008", "default"))])
    },
    "DEU_Merging_OL_02": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Merging_MT',
        "timestamp_begin": 6400,
        "timestamp_end": 6700,
        "vehicle_of_interest": 1,
        "simulation_type": "open-loop",
        "planning_meta": dict([(1, ("30008", "default"))])
    },
    "DEU_Roundabout_OL_01": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Roundabout_OF',
        "timestamp_begin": 12400,
        "timestamp_end": 17500,
        "vehicle_of_interest": 14,
        "simulation_type": "semi-open-loop",
        "planning_meta": dict([(14, ("30022", "default"))])
    },
    "DEU_Roundabout_OL_02": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Roundabout_OF',
        "timestamp_begin": 3200,
        "timestamp_end": 15300,
        "vehicle_of_interest": 12,
        "simulation_type": "open-loop",
        "planning_meta": dict([(12, ("30022", "default"))])
    },
    "USA_Intersection_EP0_01": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 8200,
        "timestamp_end": 29200,
        "vehicle_of_interest": 5,
        "simulation_type": "open-loop",
        "planning_meta": dict([(5, ("30013", "default"))])
    },
    "USA_Intersection_EP0_02": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 31500,
        "timestamp_end": 48000,
        "vehicle_of_interest": 13,
        "simulation_type": "open-loop",
        "planning_meta": dict([(13, ("30047", "default"))])
    },
    "USA_Intersection_EP0_03": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 55000,
        "timestamp_end": 76500,
        "vehicle_of_interest": 21,
        "simulation_type": "open-loop",
        "planning_meta": dict([(21, ("30029", "default"))])
    },
    "USA_Intersection_EP0_04": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 87500,
        "timestamp_end": 104000,
        "vehicle_of_interest": 28,
        "simulation_type": "open-loop",
        "planning_meta": dict([(28, ("30012", "default"))])
    },
    "USA_Intersection_EP0_05": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 182000,
        "timestamp_end": 203000,
        "vehicle_of_interest": 49,
        "simulation_type": "open-loop",
        "planning_meta": dict([(49, ("30055", "default"))])
    },
    "USA_Intersection_EP0_06": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 176100,
        "timestamp_end": 196000,
        "vehicle_of_interest": 48,
        "simulation_type": "open-loop",
        "planning_meta": dict([(48, ("30047", "default"))])
    },
    "USA_Roundabout_FT_01": {
        "source": "interaction_sim",
        "map": 'DR_USA_Roundabout_FT',
        "timestamp_begin": 25500,
        "timestamp_end": 43400,
        "vehicle_of_interest": 17,
        "simulation_type": "open-loop",
        "planning_meta": dict([(17, ("30007", "default"))])
    },
    "USA_Roundabout_FT_02": {
        "source": "interaction_sim",
        "map": 'DR_USA_Roundabout_FT',
        "timestamp_begin": 28500,
        "timestamp_end": 56000,
        "vehicle_of_interest": 19,
        "simulation_type": "open-loop",
        "planning_meta": dict([(19, ("30017", "default"))])
    },
    "USA_Intersection_EP0_80": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 114600,
        "timestamp_end": 114700,
        "vehicle_of_interest": 32,
        "simulation_type": "closed-loop",
        "planning_meta": dict([(32, ("30055", "default"))])
    },
    "USA_Intersection_EP0_81": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 114600,
        "timestamp_end": 128500,
        "vehicle_of_interest": 32,
        "simulation_type": "closed-loop",
        "planning_meta": dict([(32, ("30055", "default"))])
    },
    "DEU_Roundabout_OF_82": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Roundabout_OF',
        "timestamp_begin": 66000,
        "timestamp_end": 68500,
        "vehicle_of_interest": 30,
        "simulation_type": "closed-loop",
        "planning_meta": dict([(30, ("30022", "default")),
                               (29, ("30028", "constant-velocity"))])
    },
    "DEU_Roundabout_OF_83": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Roundabout_OF',
        "timestamp_begin": 67000,
        "timestamp_end": 68100,
        "vehicle_of_interest": 30,
        "simulation_type": "closed-loop",
        "planning_meta": dict([(30, ("30022", "default")),
                               (29, ("30028", "constant-velocity"))])
    }
}
