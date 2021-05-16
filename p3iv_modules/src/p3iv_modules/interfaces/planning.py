import abc
import p3iv_types


class PlannerInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, configurations, max_acceleration, max_deceleration, *args, **kwargs):
        pass

    @abc.abstractmethod
    def __call__(self, timestamp, motion_state, scene_model, situation_model, decision_base, *args, **kwargs):
        self.type_check(timestamp, motion_state, scene_model, situation_model, decision_base)
        pass

    @staticmethod
    def type_check(timestamp, motion_state, scene_model, situation_model, decision_base):
        assert isinstance(timestamp, int)
        assert isinstance(motion_state, p3iv_types.MotionState)
        assert isinstance(scene_model, p3iv_types.SceneModel)
        assert isinstance(situation_model, p3iv_types.SituationModel)
