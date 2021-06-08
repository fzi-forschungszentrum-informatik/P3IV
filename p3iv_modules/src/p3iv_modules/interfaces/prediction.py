import abc
import numpy as np
import p3iv_types


class PredictInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def __call__(self, timestamp, scene_model, *args, **kwargs):
        """Upon call, predict all maneuver options of all vehicles in the scene model.
        Prediction is done by using the scene models of all vehicles.

        Parameters
        -----------
        timestamp: int
            Current timestamp. Needed to compare/use prediction with ground-truth dataset
        scene_model: SceneModel
            SceneModel instance that will be converted to a SituationModel.

        Note
        ----
        Ego (host) vehicle itself is not in scene_model: scene_model is the SceneModel of ego-vehicle.
        """
        self.type_check(timestamp, scene_model)
        pass

    @staticmethod
    def type_check(timestamp, scene_model):
        """
        Utility type check function.
        """
        assert isinstance(timestamp, int)
        assert isinstance(scene_model, p3iv_types.SceneModel)
