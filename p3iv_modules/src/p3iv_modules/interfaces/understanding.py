# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import abc
import numpy as np
import p3iv_types


class SceneUnderstandingInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, dt, N, laneletmap, vehicle_id, toLanelet=None, *args, **kwargs):
        """
        Parameters
        ----------
        dt: double
            Sampling-time in [ms]
        N: int
            Number of timesteps in the horizon
        laneletmap: Lanelet2-Map
            Lanelet2 map of the current
        vehicle_id: int
            ID of ego vehicle
        toLanelet: int
            Goal lanelet ID to reach
        """
        pass

    @abc.abstractmethod
    def __call__(self, tracked_vehicles, *args, **kwargs):
        """
        Run scene understanding given tracked vehicles list.

        Parameters
        ----------
        tracked_vehicles: list
            A list of TrackedObject type
        Returns
        -------
        scene_model: SceneModel
            Scene model with curent lanelets of ego vehicle and percepted objects.
        """
        self.type_check(tracked_vehicles)
        pass

    @staticmethod
    def type_check(tracked_vehicles):
        """
        Utility type check function.
        """
        assert isinstance(tracked_vehicles, (list, np.ndarray))
        assert isinstance(tracked_vehicles[0], p3iv_types.TrackedObject)
