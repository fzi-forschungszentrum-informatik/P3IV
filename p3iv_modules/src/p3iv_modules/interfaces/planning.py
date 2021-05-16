import abc
import p3iv_types


class PlannerInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, configurations, max_acceleration, max_deceleration, *args, **kwargs):
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
        assert isinstance(timestamp, int)
        assert isinstance(motion_state, p3iv_types.MotionState)
        assert isinstance(scene_model, p3iv_types.SceneModel)
        assert isinstance(situation_model, p3iv_types.SituationModel)
