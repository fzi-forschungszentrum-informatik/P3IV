import warnings
import traceback


class VehicleModules(object):
    def __init__(self, configurations, laneletmap, vehicle):

        # set localization
        try:
            from localization.main import Localization

            self.localization = Localization(
                configurations["temporal"]["dt"],
                measurement_noise=configurations["localization"]["measurement_noise"],
                process_noise=configurations["localization"]["process_noise"],
            )
        except ImportError as e:
            print(str(traceback.format_exc()))
            self.localization = EmptyModule("Localization")

        # set perception
        try:
            from perception.main import Percept

            self.perception = Percept(
                laneletmap,
                vehicle._v_id,
                vehicle.perception.sensor_fov,
                vehicle.perception.sensor_range,
                vehicle.perception.sensor_noise,
                override_visibility=configurations["perception"]["override_visibility"],
            )
        except ImportError as e:
            print(str(traceback.format_exc()))
            self.perception = EmptyModule("Perception")

        # set understanding
        try:
            from understanding.main import Understand

            self.understanding = Understand(
                configurations["temporal"]["dt"],
                configurations["temporal"]["N"],
                laneletmap,
                vehicle._v_id,
                toLanelet=vehicle.objective.toLanelet,
            )
        except ImportError as e:
            print(str(traceback.format_exc()))
            self.understanding = EmptyModule("Understanding")

        # set prediction
        try:
            from prediction.main import Predict

            self.prediction = Predict(
                configurations["temporal"]["dt"],
                configurations["temporal"]["N"],
                configurations["map"],
                configurations["prediction"],
            )

        except ImportError as e:
            print(str(traceback.format_exc()))
            self.prediction = EmptyModule("Prediction")

        # set decision
        try:
            from decision_making.main import Decide

            self.decision = Decide(
                vehicle.characteristics.max_acceleration,
                vehicle.characteristics.max_deceleration,
                vehicle.objective.set_speed,
                configurations["temporal"]["dt"],
                configurations["temporal"]["N"],
                configurations["temporal"]["N_pin_future"],
                configurations["decision_making"]["astar_initialization"],
            )
        except ImportError as e:
            print(str(traceback.format_exc()))
            self.decision = EmptyModule("Decision")

        # set planner
        try:
            from planner.main import Plan

            self.planner = Plan(
                configurations,
                vehicle.characteristics.max_acceleration,
                vehicle.characteristics.max_deceleration,
                get_planner_type(configurations, vehicle),
            )
        except ImportError as e:
            print(str(traceback.format_exc()))
            self.planner = EmptyModule("Planner")

        # set action
        try:
            from action.main import Act

            self.action = Act()
        except ImportError as e:
            print(str(traceback.format_exc()))
            self.action = EmptyModule("Action")


class EmptyModule(object):
    def __init__(self, module_name, *args, **kwargs):
        self._module_name = module_name
        pass

    def __call__(self, *args, **kwargs):
        warnings.warn(str(self._module_name) + " is not defined.")
        return None


def get_planner_type(configurations, vehicle):
    if vehicle.v_id in configurations["planning_meta"].keys():
        if configurations["planning_meta"][vehicle.v_id][1] == "default":
            return configurations["planning"]["solver"]
        else:
            return configurations["planning_meta"][vehicle.v_id][1]
    else:
        return "open-loop"
