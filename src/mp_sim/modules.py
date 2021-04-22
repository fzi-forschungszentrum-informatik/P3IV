class VehicleModules(object):
    def __init__(self, configurations, laneletmap, vehicle):

        # set localization
        try:
            from localization.main import Localization
            self.localization = Localization(configurations["temporal"]["dt"],
                                             measurement_noise=configurations["localization"]["measurement_noise"],
                                             process_noise=configurations["localization"]["process_noise"])
        except ImportError as e:
            print(str(e))

        # set perception
        try:
            from perception.main import Percept
            self.perception = Percept(laneletmap,
                                      vehicle._v_id,
                                      vehicle.perception.sensor_fov,
                                      vehicle.perception.sensor_range,
                                      vehicle.perception.sensor_noise,
                                      override_visibility=configurations['perception']['override_visibility'])
        except ImportError as e:
            print(str(e))

        # set understanding
        try:
            from understanding.main import Understand
            self.understanding = Understand(configurations["temporal"]["dt"],
                                            configurations["temporal"]
                                            ["N"],
                                            laneletmap,
                                            vehicle._v_id,
                                            toLanelet=vehicle.objective.toLanelet)
        except ImportError as e:
            print(str(e))

        # set prediction
        try:
            from prediction.main import Predict
            self.prediction = Predict(configurations["temporal"]["dt"],
                                      configurations["temporal"]["N"],
                                      configurations["map"],
                                      configurations["prediction"])
        except ImportError as e:
            print(str(e))

        # set decision
        try:
            from decision_making.main import Decide
            self.decision = Decide(vehicle.characteristics.max_acceleration,
                                   vehicle.characteristics.max_deceleration,
                                   vehicle.objective.set_speed,
                                   configurations["temporal"]["dt"],
                                   configurations["temporal"]["N"],
                                   configurations["temporal"]["N_pin_future"],
                                   configurations["decision_making"]["astar_initialization"])
        except ImportError as e:
            print(str(e))

        # set planner
        try:
            from planner.main import Plan
            self.planner = Plan(configurations,
                                vehicle.characteristics.max_acceleration,
                                vehicle.characteristics.max_deceleration,
                                get_planner_type(configurations, vehicle))
        except ImportError as e:
            print(str(e))

        # set action
        try:
            from action.main import Act
            self.action = Act()
        except ImportError as e:
            print(str(e))


def get_planner_type(configurations, vehicle):
    if vehicle.v_id in configurations['planning_meta'].keys():
        if configurations['planning_meta'][vehicle.v_id][1] == 'default':
            return configurations["planning"]["solver"]
        else:
            return configurations['planning_meta'][vehicle.v_id][1]
    else:
        return "open-loop"
