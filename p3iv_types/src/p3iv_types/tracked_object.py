# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np


class ExistenceProbabilityBase:
    __slots__ = ["_existence_probability"]


class ExistenceProbability(ExistenceProbabilityBase, object):
    """
    Abstract class to store existence probability of a detected object.

    Properties
    ----------
    existence_probability : float64
        The probability that the object really exists.
    """

    __slots__ = []

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


class TrackedObject(ExistenceProbability):
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

    @property
    def id(self):
        return self._object_id

    @id.setter
    def id(self, object_id):
        assert isinstance(object_id, int)
        self._object_id = object_id
