# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import abc
import p3iv_types


class PlannerInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, v_id, v_width, v_length, configurations, max_acceleration, max_deceleration, *args, **kwargs):
        pass

    @abc.abstractmethod
    def __call__(self, timestamp, motion_state, scene_model, situation_model, decision_base, *args, **kwargs):
        """
        Perform planning given current scene model, situation model and decision base.

        Parameters
        ----------
        timestamp: int
            Current timestamp value.
        motion_state: MotionState
            Current motion state of the vehicle.
        scene_model: SceneModel
            Scene model built up for the current timestamp.
        situation_model: SituationModel
            Situation model that includes prediction of vehicles in the scene_model.
        decision_base: DecisionBase
            Decision base that includes driving intentions of the ego vehicle.

        Returns
        -------
        motion_plans: MotionPlans
            A container that contains motions of different homotopy classes.

        """
        self.type_check(timestamp, motion_state, scene_model, situation_model, decision_base)
        pass

    @staticmethod
    def type_check(timestamp, motion_state, scene_model, situation_model, decision_base):
        """
        Utility type check function.
        """
        assert isinstance(timestamp, int)
        assert isinstance(motion_state, p3iv_types.MotionState)
        assert isinstance(scene_model, p3iv_types.SceneModel)
        assert isinstance(situation_model, p3iv_types.SituationModel)

    @staticmethod
    def overwrite_with_current_state(motion_plan, current_state):
        """
        Components of motion plans can be calculated with finite differences.
        Overwrite initial values with current state.
        """
        motion_plan.motion.position.mean[0] = current_state.position.mean
        motion_plan.motion.position.covariance[0] = current_state.position.covariance
        motion_plan.motion.velocity.mean[0] = current_state.velocity.mean
        motion_plan.motion.velocity.covariance[0] = current_state.velocity.covariance
        motion_plan.motion.yaw.mean[0] = current_state.yaw.mean
        motion_plan.motion.yaw.covariance[0] = current_state.yaw.covariance
