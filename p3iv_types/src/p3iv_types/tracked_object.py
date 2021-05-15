from __future__ import division

import numpy as np
import random
from matplotlib import colors as mcolors


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


def get_color(index):
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    return colors.keys()[index]


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
        self._color = get_color(random.randint(0, 155))

    @property
    def id(self):
        return self._object_id

    @id.setter
    def id(self, object_id):
        assert isinstance(object_id, int)
        self._object_id = object_id

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        assert isinstance(color, (unicode, str))
        self._color = color
