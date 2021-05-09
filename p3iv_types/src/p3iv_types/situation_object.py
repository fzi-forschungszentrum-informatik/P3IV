from __future__ import division
import warnings
from p3iv_types.scene_object import SceneObject


class SituationObject(object):
    """
    v_id: int
        Vehicle ID
    maneuvers: ManeuverHypotheses
        Current maneuver hypothesis of the current timestep
    """

    __slots__ = ["v_id", "maneuvers", "crossing_voi_route"]

    def __init__(self, *args, **kwargs):
        if type(args[0]) is SceneObject:
            self.v_id = args[0].v_id
            warnings.warn("todo - crossing voi route of situation object --> do that for path options")
            self.crossing_voi_route = args[0].crossing_voi_route
