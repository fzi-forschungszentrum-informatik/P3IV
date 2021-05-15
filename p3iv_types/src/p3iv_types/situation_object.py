from __future__ import division
import warnings
import itertools
from p3iv_types.scene_object import SceneObject
from p3iv_types.tracked_object import TrackedObject
# from p3iv_types.vehicle import TrackedVehicle


class SituationObject(TrackedObject):
    """
    _object_id: int
        Object ID
    maneuvers: ManeuverHypotheses
        Current maneuver hypothesis of the current timestep
    """

    __slots__ = ["_maneuvers"]

    def __init__(self, *args, **kwargs):
        if type(args[0]) is SceneObject:
            all_slots = list(itertools.chain.from_iterable(getattr(t, "__slots__", ()) for t in type(self).__mro__))
            for attr in all_slots:
                if hasattr(args[0], attr):
                    setattr(self, attr, getattr(args[0], attr))
        else:
            self._maneuvers = None
            self._object_id = args[0]
            self._color = args[1]
            self._existence_probability = args[3]
            # self._length = args[4]
            # self._width = args[5]

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
