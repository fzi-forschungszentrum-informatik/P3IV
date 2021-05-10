from __future__ import division
import warnings
from p3iv_types.scene_object import SceneObject


class SituationObject(object):
    """
    _object_id: int
        Object ID
    maneuvers: ManeuverHypotheses
        Current maneuver hypothesis of the current timestep
    """

    __slots__ = ["_object_id", "maneuvers", "crossing_voi_route"]

    def __init__(self, *args, **kwargs):
        if type(args[0]) is SceneObject:
            self._object_id = args[0].id
            warnings.warn("todo - crossing voi route of situation object --> do that for path options")
            self.crossing_voi_route = args[0].crossing_voi_route

    # todo add init with... See prediction test cases! Make this more generic

    @property
    def id(self):
        return self._object_id

    @id.setter
    def id(self, object_id):
        assert isinstance(object_id, int)
        self._object_id = object_id
