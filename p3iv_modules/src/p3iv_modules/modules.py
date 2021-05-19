from __future__ import absolute_import
import warnings
import traceback
import importlib
import p3iv_modules.interfaces as interfaces


class VehicleModules(object):
    def __init__(self, configurations, laneletmap, vehicle):

        # set perception
        try:
            try:
                # try to import limited visibility perception -- considers visible fields
                # will fail, if cgal is not installed
                from p3iv_modules.perception.limited import Percept

            except ImportError:
                # fallback to perfect perception
                from p3iv_modules.perception.perfect import Percept

            self.perception = Percept(
                vehicle.id,
                laneletmap,
                vehicle.perception.sensor_fov,
                vehicle.perception.sensor_range,
                vehicle.perception.sensor_noise,
            )

            assert isinstance(self.perception, interfaces.PerceptInterface)

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
                vehicle.id,
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
            try:
                # search externally
                module_path = configurations["prediction"]["module_name"] + "decide"
                Decide = getattr(importlib.import_module(module_path), "Decide")
            except ImportError:
                # search in p3iv_modules as fallback
                module_path = "p3iv_modules.decision.decision_making"
                Decide = getattr(importlib.import_module(module_path), "Decide")

            self.decision = Decide()

            assert isinstance(self.decision, interfaces.DecisionMakingInterface)
        except ImportError as e:
            print(str(traceback.format_exc()))
            self.decision = EmptyModule("Decision")

        # set planner
        try:
            planner_type = get_planner_type(configurations, vehicle)
            try:
                # search externally
                module_path = "planner_" + planner_type + ".planner"
                Planner = getattr(importlib.import_module(module_path), "Planner")
            except ImportError:
                # search in p3iv_modules as fallback
                module_path = "p3iv_modules.planner." + planner_type
                Planner = getattr(importlib.import_module(module_path), "Planner")

            self.planner = Planner(
                configurations,
                vehicle.characteristics.max_acceleration,
                vehicle.characteristics.max_deceleration,
            )
            assert isinstance(self.planner, interfaces.PlannerInterface)

        except ImportError as e:
            print(str(traceback.format_exc()))
            self.planner = EmptyModule("Planner")

        # set action
        try:
            Act = getattr(importlib.import_module("p3iv_modules.action.act"), "Act")
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
    if vehicle.id in configurations["planning_meta"].keys():
        if configurations["planning_meta"][vehicle.id][1] == "default":
            return configurations["planning"]["type"]
        else:
            return configurations["planning_meta"][vehicle.id][1]
    else:
        return configurations["planning"]["type"]
