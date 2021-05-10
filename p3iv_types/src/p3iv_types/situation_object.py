from __future__ import division
import warnings
import itertools
from p3iv_types.scene_object import SceneObject
from p3iv_types.tracked_object import TrackedObject


class SituationObject(TrackedObject):
    """
    _object_id: int
        Object ID
    maneuvers: ManeuverHypotheses
        Current maneuver hypothesis of the current timestep
    """

    __slots__ = ["_maneuvers", "_crossing_voi_route"]

    def __init__(self, *args, **kwargs):
        if type(args[0]) is SceneObject:
            self.id = args[0].id
            warnings.warn("todo - crossing voi route of situation object --> do that for path options")
            self.crossing_voi_route = args[0].crossing_voi_route

    # todo add init with... See prediction test cases! Make this more generic

    def __setattr__(self, name, value):
        # modify setattr for multiple inheritence

        # get all slots
        all_slots = list(itertools.chain.from_iterable(getattr(t, "__slots__", ()) for t in type(self).__mro__))

        # cast slots iterable to list
        if name in all_slots:
            object.__setattr__(self, name, value)
        else:
            # call property if name is not in slots
            super(SituationObject, self).__setattr__(name, value)

    @property
    def maneuvers(self):
        return self._maneuvers

    @maneuvers.setter
    def maneuvers(self, maneuvers):
        self._maneuvers = maneuvers

    @property
    def crossing_voi_route(self):
        return self._crossing_voi_route

    @crossing_voi_route.setter
    def crossing_voi_route(self, crossing_voi_route):
        self._crossing_voi_route = crossing_voi_route
