from __future__ import absolute_import
import numpy as np
from p3iv_types.decision_base import DecisionBase
from p3iv_modules.interfaces import DecisionMakingInterface


class Decide(DecisionMakingInterface):

    """
    Each situation object has a prediction in the form of Truncated Gaussian Mixture Data.
    Decision making module checks the maneuver probabilities and either:
    * reduces the maneuver hypotheses to a single maneuver and applies divide&conquer
    * passes both of the variants for maneuver neutral planning
    for each vehicle.
    It further
    * truncates the object prediction distributions according to intersection begins
    * identifies relevant vehicles and fuses the predictions of distinct objects into a unified base.
    """

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, motion_state, scene_model, situation_model, *args, **kwargs):
        decision_base = DecisionBase()

        # take only the relevant interval of lanelets for efficiency
        # todo: calculate reachable max
        # index_current_ll = scene_model.laneletpath_entire.where(
        #    scene_model.current_lanelets.id)
        # laneletpath_destination = scene_model.laneletpath_entire[index_current_ll:]

        decision_base.set_driving_corridor(scene_model.route_option.laneletsequence)
        return decision_base

        # combinatorial_alternatives = self.decide(scene_model, situation_model)

    """
    def decide(self, scene_model, situation_model, to_lanelet):
        combinatorial_alternatives = self.__maneuver_identifier(
            scene_model, situation_model)
        self.__maneuver_extractor.get_maneuver_options(
            scene_model, combinatorial_alternatives, situation_model)
        return combinatorial_alternatives
    """
