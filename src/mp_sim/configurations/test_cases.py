test_cases = {

    "DEU_Merging_CL_01": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Merging_MT_extended',
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
        "map": 'DR_DEU_Merging_MT_extended',
        "timestamp_begin": 4400,
        "timestamp_end": 8400,
        "vehicle_of_interest": 1,
        "open_loop": True,
        "toLanelet": dict([(1, "30008")])
    },
    "DEU_Merging_OL_02": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Merging_MT_extended',
        "timestamp_begin": 6400,
        "timestamp_end": 6700,
        "vehicle_of_interest": 1,
        "open_loop": True,
        "toLanelet": dict([(1, "30008")])
    },
    "DEU_Roundabout_OL_01": {
        "source": "interaction_sim",
        "map": 'DR_DEU_Roundabout_OF_extended',
        "timestamp_begin": 12400,
        "timestamp_end": 15400,
        "vehicle_of_interest": 14,
        "open_loop": True,
        "toLanelet": dict([(14, "30022")])
    }
}
