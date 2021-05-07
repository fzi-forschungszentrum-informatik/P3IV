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
    Contains information on a detected vehicle.

    Attributes
    ---------
    _v_id : int
        Vehicle id
    _color : str
        Vehicle color
    """

    __slots__ = ["_v_id", "_color"]

    def __init__(self):
        super(TrackedObject, self).__init__()
        self._v_id = 0
        self._color = "black"  # override appearance

    @property
    def v_id(self):
        return self._v_id

    @v_id.setter
    def v_id(self, vehicle_id):
        assert isinstance(vehicle_id, int)
        self._v_id = vehicle_id
