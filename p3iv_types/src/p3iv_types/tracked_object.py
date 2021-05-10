from __future__ import division
import numpy as np
from p3iv_types.vehicle import VehicleAppearance


class ExistenceProbability(object):
    """
    Existence probability of a detected vehicle.

    Properties
    ----------
    existence_probability : float64
        The probability that the vehicle really exists.
    """

    # Don't define slots for multiple inheritence of TrackedObject

    def __init__(self):
        super(ExistenceProbability, self).__init__()
        self._existence_probability = 1.0

    @property
    def existence_probability(self):
        return self._existence_probability

    @existence_probability.setter
    def existence_probability(self, probability):
        assert 0.0 <= probability <= 1.0
        self._existence_probability = probability


class TrackedObject(VehicleAppearance, ExistenceProbability):
    """
    Contains information on a detected object.

    Attributes
    ---------
    _object_id : int
        Object id
    _color : str
        Object color
    """

    __slots__ = ["_object_id", "_color"]

    def __init__(self):
        super(TrackedObject, self).__init__()
        self._object_id = 0
        self._color = "black"  # override appearance

    def __setattr__(self, name, value):
        # modify setattr for multiple inheritence

        # get all slots
        all_slots = itertools.chain.from_iterable(getattr(t, "__slots__", ()) for t in type(self).__mro__)

        # cast slots iterable to list
        if name in list(all_slots):
            object.__setattr__(self, name, value)
        else:
            # call property if name is not in slots
            super(TrackedObject, self).__setattr__(name, value)

    @property
    def id(self):
        return self._object_id

    @id.setter
    def id(self, object_id):
        assert isinstance(object_id, int)
        self._object_id = object_id
