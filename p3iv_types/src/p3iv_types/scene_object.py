from __future__ import division
import itertools
import numpy as np
from copy import deepcopy
from vehicle import VehicleAppearance
from tracked_object import TrackedObject


class SceneObject(TrackedObject, VehicleAppearance):
    """
    Contains information on a detected vehicle.

    Attributes
    ---------
    progress: Univariate normal distribution
        Current longitudinal position.
    current_lanelets : list
        Contains list of current Lanelets the object might be on.
    route_options: List
        Route options the vehicle may pick in the future
    route_scenes: List
        List of SceneModel for every route option
    """

    __slots__ = [
        "existence_probability",
        "state",
        "progress",
        "current_lanelets",
        "route_options",
        "route_scenes",
    ]

    def __init__(self):
        super(SceneObject, self).__init__()
        self.progress = 0.0
        self.current_lanelets = []
        self.route_options = []
        self.route_scenes = []

    def __getstate__(self):
        self.current_lanelets = [ll.id for ll in list(self.current_lanelets)]
        all_slots = itertools.chain.from_iterable(getattr(t, "__slots__", ()) for t in type(self).__mro__)
        state = {attr: getattr(self, attr) for attr in all_slots if hasattr(self, attr)}
        return state

    def __setstate__(self, state):
        """Implement for load in pickle."""
        for k, v in state.iteritems():
            setattr(self, k, v)

    def __deepcopy__(self, memo):
        """
        Modify __deepcopy__ as a workaround for pickling boost.python instances.
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        all_slots = itertools.chain.from_iterable(getattr(t, "__slots__", ()) for t in type(self).__mro__)
        for k in all_slots:
            if (k is "route_options") or (k is "state"):
                v = getattr(self, k)
                # deepcopy the ones, that will be modified while evaluating scene model of other vehicles
                setattr(result, k, deepcopy(v, memo))
            elif k is "route_scenes":
                setattr(result, k, [])
            else:
                v = getattr(self, k)
                setattr(result, k, v)
        return result
