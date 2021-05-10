from __future__ import division
import itertools
import numpy as np
from copy import deepcopy
from vehicle import VehicleAppearance
from tracked_object import TrackedObject


class CrossingVOIRoute(object):
    """
    Store info on when the route of scene-object crosses the route of a VOI.
    The 'begin' and 'end' points are calculated in the coordinates of VOI.
    """

    __slots__ = ["_begin", "_end"]

    def __init__(self):
        self._begin = -np.inf
        self._end = np.inf

    @property
    def begin(self):
        return self._begin

    @begin.setter
    def begin(self, begin):
        assert isinstance(begin, float)
        self._begin = begin

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        assert isinstance(end, float)
        self._end = end


class SceneObject(TrackedObject, VehicleAppearance):
    """
    Contains information on a detected vehicle.

    Attributes
    ---------
    progress: Univariate normal distribution
        Current longitudinal position.
    current_lanelets : list
        Contains list of current Lanelets the object might be on.
    laneletsequences: List
        LaneletSequence(s) the vehicle may pick in the future
    laneletsequence_scenes: List
        List of SceneModel for every path_option
    crossing_voi_route:  CrossingVOIRoute
        An object defining for which values along centerline it will cross own path. The value is filled for scene
        objects inside a SceneModel.
    """

    __slots__ = [
        "existence_probability",
        "state",
        "progress",
        "current_lanelets",
        "laneletsequences",
        "laneletsequence_scenes",
        "crossing_voi_route",
        "has_right_of_way",
    ]

    def __init__(self):
        super(SceneObject, self).__init__()
        self.progress = 0.0
        self.current_lanelets = []
        self.laneletsequences = []
        self.laneletsequence_scenes = []
        self.crossing_voi_route = CrossingVOIRoute()
        self.has_right_of_way = None

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
            if (k is "crossing_voi_route") or (k is "state"):
                v = getattr(self, k)
                # deepcopy the ones, that will be modified while evaluating scene model of other vehicles
                setattr(result, k, deepcopy(v, memo))
            elif k is "laneletsequence_scenes":
                setattr(result, k, [])
            else:
                v = getattr(self, k)
                setattr(result, k, v)
        return result
