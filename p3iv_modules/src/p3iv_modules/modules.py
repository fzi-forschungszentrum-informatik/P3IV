# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import sys
import warnings
import traceback
import importlib
import p3iv_modules.interfaces as interfaces
from termcolor import colored

# for backwards compatibility with Python2
if sys.version_info < (3,):
    ModuleNotFoundError = ImportError


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
                configurations["perception"]["position_sigma_longitudinal"],
                configurations["perception"]["position_sigma_lateral"],
                configurations["perception"]["position_cross_correlation"],
                configurations["perception"]["velocity_sigma_longitudinal"],
                configurations["perception"]["velocity_sigma_lateral"],
                configurations["perception"]["velocity_cross_correlation"],
                configurations["localization"]["position_sigma_longitudinal"],
                configurations["localization"]["position_sigma_lateral"],
                configurations["localization"]["position_cross_correlation"],
                configurations["localization"]["velocity_sigma_longitudinal"],
                configurations["localization"]["velocity_sigma_lateral"],
                configurations["localization"]["velocity_cross_correlation"],
                laneletmap,
                vehicle.perception.sensors,
            )

            assert isinstance(self.perception, interfaces.PerceptInterface)

        except ImportError as e:
            print((str(traceback.format_exc())))
            self.perception = EmptyModule("Perception")

        # set understanding
        try:
            understanding_type = configurations["understanding"]["type"]
            try:
                # search in internal modules (p3iv_modules) first
                module_path = "p3iv_modules.understanding." + understanding_type
                Understand = getattr(importlib.import_module(module_path), "Understand")
            except (ModuleNotFoundError, ImportError, KeyError):
                # search externally
                # todo: module_path = "understanding_" + understanding_type + ".understand"
                module_path = "understanding_" + understanding_type + ".understand"
                Understand = getattr(importlib.import_module(module_path), "Understand")

            self.understanding = Understand(
                configurations["temporal"]["dt"],
                configurations["temporal"]["N"],
                laneletmap,
                vehicle.id,
                toLanelet=vehicle.objective.toLanelet,
                save_dir=configurations["save_dir"],
            )
            assert isinstance(self.understanding, interfaces.SceneUnderstandingInterface)

        except ImportError as e:
            print((str(traceback.format_exc())))
            msg = "Is the understaning pkg 'understanding_" + str(understanding_type) + "' in your workspace?"
            msg += "\nIs your ws is built & sourced?"
            print((colored(msg, "red")))
            self.understanding = EmptyModule("Understand")

        # set prediction
        try:
            prediction_type = configurations["prediction"]["type"]
            try:
                # search in internal modules (p3iv_modules) first
                module_path = "p3iv_modules.prediction." + prediction_type
                Prediction = getattr(importlib.import_module(module_path), "Predict")

            except ImportError:
                # search externally
                module_path = "prediction_" + prediction_type + ".prediction"
                Prediction = getattr(importlib.import_module(module_path), "Predict")

            self.prediction = Prediction(configurations, laneletmap)
            assert isinstance(self.prediction, interfaces.PredictInterface)

        except ImportError as e:
            print((str(traceback.format_exc())))
            msg = "Is the prediction pkg 'prediction_" + str(prediction_type) + "' in your workspace?"
            msg += "\nIs your ws is built & sourced?"
            print((colored(msg, "red")))
            self.prediction = EmptyModule("Prediction")

        # set decision
        try:
            decision_type = configurations["decision_making"]["type"]
            try:
                # search in internal modules (p3iv_modules) first
                module_path = "p3iv_modules.decision." + decision_type
                Decide = getattr(importlib.import_module(module_path), "Decide")
            except ImportError:
                # search externally
                module_path = str(configurations["decision_making"]["pkg_name"]) + "decide"
                Decide = getattr(importlib.import_module(module_path), "Decide")

            self.decision = Decide()

            assert isinstance(self.decision, interfaces.DecisionMakingInterface)
        except ImportError as e:
            print((str(traceback.format_exc())))
            self.decision = EmptyModule("Decision")

        # set planner
        try:
            planner_type = get_planner_type(configurations, vehicle)
            try:
                # search in internal modules (p3iv_modules) first
                module_path = "p3iv_modules.planner." + planner_type
                Planner = getattr(importlib.import_module(module_path), "Planner")
            except ImportError:
                # search externally
                module_path = "planner_" + planner_type + ".planner"
                Planner = getattr(importlib.import_module(module_path), "Planner")

            self.planner = Planner(
                vehicle.id,
                vehicle.appearance.width,
                vehicle.appearance.length,
                configurations,
                vehicle.characteristics.max_acceleration,
                vehicle.characteristics.max_deceleration,
                laneletmap,
            )
            assert isinstance(self.planner, interfaces.PlannerInterface)

        except ImportError as e:
            print((str(traceback.format_exc())))
            msg = "Is the planner pkg 'planner_" + str(planner_type) + "' in your workspace?"
            msg += "\nIs your ws is built & sourced?"
            print((colored(msg, "red")))
            self.planner = EmptyModule("Planner")

        # set action
        try:
            Act = getattr(importlib.import_module("p3iv_modules.action.act"), "Act")
            self.action = Act()

        except ImportError as e:
            print((str(traceback.format_exc())))
            self.action = EmptyModule("Action")


class EmptyModule(object):
    def __init__(self, module_name, *args, **kwargs):
        self._module_name = module_name
        pass

    def __call__(self, *args, **kwargs):
        warnings.warn(str(self._module_name) + " is not defined.")
        return None


def get_planner_type(configurations, vehicle):
    if vehicle.id in list(configurations["meta_state"].keys()):
        if configurations["meta_state"][vehicle.id][1] == "default":
            return configurations["planning"]["type"]
        else:
            return configurations["meta_state"][vehicle.id][1]
    else:
        return configurations["planning"]["type"]
