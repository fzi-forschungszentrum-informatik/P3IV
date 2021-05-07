from __future__ import division
import numpy as np
from copy import deepcopy
from understanding.types.external.p3iv_utils import VehicleAppearance


class CrossingVOIRoute(object):
    """
    Store info on when the route of scene-object crosses the route of a VOI.
    The 'begin' and 'end' points are calculated in the coordinates of VOI.
    """

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


class SceneObject(VehicleAppearance):
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

    # todo: inherit from VehicleAppereance
    """
    # todo: add slots
    __slots__ = [
        "__dict__",
        "_v_id",
        "progress",
        "current_lanelets",
        "laneletsequences",
        "laneletsequence_scenes",
        "crossing_voi_route",
        "has_right_of_way",
    ]
    """

    def __init__(self):
        super(SceneObject, self).__init__()
        self._v_id = 0
        self._color = "black"  # override appearance

        self.progress = 0.0
        self.current_lanelets = []
        self.laneletsequences = []
        self.laneletsequence_scenes = []
        self.crossing_voi_route = CrossingVOIRoute()
        self.has_right_of_way = None

    def __getstate__(self):
        if isinstance(self.current_lanelets, list):
            self.current_lanelets = [ll.id for ll in list(self.current_lanelets)]
        else:
            self.current_lanelets = self.current_lanelets.id
        return self.__dict__

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        for k, v in self.__dict__.items():
            if (k is "crossing_voi_route") or (k is "state"):
                setattr(result, k, deepcopy(v, memo))
            elif k is "laneletsequence_scenes":
                setattr(result, k, [])
            else:
                setattr(result, k, v)
        return result

    @property
    def v_id(self):
        return self._v_id

    @v_id.setter
    def v_id(self, vehicle_id):
        assert isinstance(vehicle_id, int)
        self._v_id = vehicle_id
