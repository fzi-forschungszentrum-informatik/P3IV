import abc
import numpy as np
import p3iv_types


class PerceptInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def __call__(self, timestamp, ground_truth, *args, **kwargs):
        """
        Perform environment perception and return an environment model.

        Parameters
        ----------
        timestamp: int
            Current timestamp value.
        ground_truth: GroundTruth
            Ground truth data of the current timestamp.

        Returns
        -------
        environment_model: EnvironmentModel
            Environment model with visible areas, percepted objects.
        """
        self.type_check(timestamp, ground_truth)
        pass

    @staticmethod
    def type_check(timestamp, ground_truth):
        assert isinstance(timestamp, int)
        assert isinstance(ground_truth, p3iv_types.GroundTruth)
