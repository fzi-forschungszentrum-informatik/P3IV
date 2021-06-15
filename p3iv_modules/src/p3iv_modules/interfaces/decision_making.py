import abc
import p3iv_types


class DecisionMakingInterface(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, configurations, max_acceleration, max_deceleration, *args, **kwargs):
        pass

    @abc.abstractmethod
    def __call__(self, motion_state, scene_model, situation_model, *args, **kwargs):
        """
        Perform decision making given current motion state, scene model, and situation model.

        Parameters
        ----------
        motion_state: MotionState
            Current motion state of the vehicle.
        scene_model: SceneModel
            Scene model built up for the current timestamp.
        situation_model: SituationModel
            Situation model that includes prediction of vehicles in the scene_model.


        Returns
        -------
        decision_base: DecisionBase
            Decision base that includes driving intentions of the ego vehicle.

        """
        self.type_check(motion_state, scene_model, situation_model)
        pass

    @staticmethod
    def type_check(motion_state, scene_model, situation_model):
        """
        Utility type check function.
        """
        assert isinstance(motion_state, p3iv_types.MotionState)
        assert isinstance(scene_model, p3iv_types.SceneModel)
        assert isinstance(situation_model, p3iv_types.SituationModel)
