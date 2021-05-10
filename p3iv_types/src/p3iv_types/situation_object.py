from __future__ import division
import warnings
from p3iv_types.scene_object import SceneObject
from p3iv_types.tracked_object import TrackedObject


class SituationObject(TrackedObject):
    """
    _object_id: int
        Object ID
    maneuvers: ManeuverHypotheses
        Current maneuver hypothesis of the current timestep
    """

    __slots__ = ["maneuvers", "crossing_voi_route"]

    def __init__(self, *args, **kwargs):
        if type(args[0]) is SceneObject:
            self.id = args[0].id
            warnings.warn("todo - crossing voi route of situation object --> do that for path options")
            self.crossing_voi_route = args[0].crossing_voi_route

    # todo add init with... See prediction test cases! Make this more generic
