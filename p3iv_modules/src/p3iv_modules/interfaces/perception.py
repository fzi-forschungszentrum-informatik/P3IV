import abc
import numpy as np
import p3iv_types


class PerceptInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        ego_v_id: int
            ID of the vehicle, which the perception module belongs to
        per_pos_sigma_x:
            Position perception variance in longitudinal direction
        per_pos_sigma_y:
            Position perception variance in lateral direction
        per_pos_cross_corr:
            Position perception cross-correlation factor
        per_vel_sigma_x:
            Velocity perception variance in longitudinal direction
        per_vel_sigma_y:
            Velocity perception variance in lateral direction
        per_vel_cross_corr:
            Velocity perception cross-correlation factor
        loc_pos_sigma_x:
            Position localization variance in longitudinal direction
        loc_pos_sigma_y:
            Position localization variance in lateral direction
        loc_pos_cross_corr:
            Position localization cross-correlation factor
        loc_vel_sigma_x:
            Velocity localization variance in longitudinal direction
        loc_vel_sigma_y:
            Velocity localization variance in lateral direction
        loc_vel_cross_corr:
            Velocity localization cross-correlation factor
        """
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
        """
        Utility type check function.
        """
        assert isinstance(timestamp, int)
        assert isinstance(ground_truth, p3iv_types.GroundTruth)
