test_cases = {

    "DEU_Merging_CL_01": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Merging_MT',
        "timestamp_begin": 4400,
        "timestamp_end": 4400,
        "vehicle_of_interest": 1,
        "open_loop": False,
        "toLanelet": dict([(1, "30008"),  # closed-loop planning is performed only for vehicles that are defined here
                           (2, "30008"),
                           (3, "30008")])
    },
    "DEU_Merging_OL_01": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Merging_MT',
        "timestamp_begin": 4400,
        "timestamp_end": 8400,
        "vehicle_of_interest": 1,
        "open_loop": True,
        "toLanelet": dict([(1, "30008")])
    },
    "DEU_Merging_OL_02": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Merging_MT',
        "timestamp_begin": 6400,
        "timestamp_end": 6700,
        "vehicle_of_interest": 1,
        "open_loop": True,
        "toLanelet": dict([(1, "30008")])
    },
    "DEU_Roundabout_OL_01": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Roundabout_OF',
        "timestamp_begin": 12400,
        "timestamp_end": 13500,
        "vehicle_of_interest": 14,
        "open_loop": True,
        "toLanelet": dict([(14, "30022")])
    },
    "DEU_Roundabout_OL_02": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Roundabout_OF',
        "timestamp_begin": 3200,
        "timestamp_end": 15300,
        "vehicle_of_interest": 12,
        "open_loop": True,
        "toLanelet": dict([(12, "30022")])
    },
    "USA_Intersection_EP0_01": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 8200,
        "timestamp_end": 29200,
        "vehicle_of_interest": 5,
        "open_loop": True,
        "toLanelet": dict([(5, "30013")])
    },
    "USA_Intersection_EP0_02": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 31500,
        "timestamp_end": 48000,
        "vehicle_of_interest": 13,
        "open_loop": True,
        "toLanelet": dict([(13, "30047")])
    },
    "USA_Intersection_EP0_03": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 55000,
        "timestamp_end": 76500,
        "vehicle_of_interest": 21,
        "open_loop": True,
        "toLanelet": dict([(21, "30029")])
    },
    "USA_Intersection_EP0_04": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 87500,
        "timestamp_end": 104000,
        "vehicle_of_interest": 28,
        "open_loop": True,
        "toLanelet": dict([(28, "30012")])
    },
    "USA_Intersection_EP0_05": {
        "source": "interaction_sim",
        "map": 'DR_USA_Intersection_EP0',
        "timestamp_begin": 176100,
        "timestamp_end": 196000,
        "vehicle_of_interest": 48,
        "open_loop": True,
        "toLanelet": dict([(48, "30047")])
    }
}
