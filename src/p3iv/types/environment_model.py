from __future__ import division
from p3iv.types.tracked_object import TrackedObject


class EnvironmentModel(object):
    """
    Contains information on traffic rules, visible regions,the laneletmap and information on lanelets
    that are already driven and those that lead to goal lanelet, including the driven ones.

    Attributes
    ----------
    _tracked_objects: dict
        dictionary of TrackedObjects
    visible areas: list
        a list that contains the Cartesian coordinates of visibility polygon
    polyvision: VisibleArea
        instance of visibility calculator VisibleArea from package pypolyvision
    laneletmap: LaneletMap
        Lanelet2 of the environment
    """

    def __init__(self, vehicle_id=None, visible_areas=None, polyvision=None, laneletmap=None):
        self._tracked_objects = {}
        self._vehicle_id = vehicle_id
        self.polyvision = polyvision
        self.visible_areas = visible_areas
        self.laneletmap = laneletmap

    def __getstate__(self):
        """Implement for dump in pickle. Lanelet2 and Polyvision are implemented in C++ and cannot be pickled.
        """
        delattr(self, 'laneletmap')
        delattr(self, 'polyvision')
        return self.__dict__

    def __setstate__(self, d):
        """Implement for load in pickle.
        """
        self.__dict__ = d

    @property
    def tracked_objects(self):
        return self._tracked_objects

    def add_object(self, v_id, color, length, width, motion):
        self._tracked_objects[v_id] = self.create_object(v_id, color, length, width, motion)

    @staticmethod
    def create_object(v_id, color, length, width, motion):
        tracked_object = TrackedObject()
        tracked_object.v_id = v_id
        tracked_object.color = color
        tracked_object.length = length
        tracked_object.width = width
        tracked_object.motion = motion
        tracked_object.existence_probability = 1.0
        return tracked_object

    def objects(self, relative_to=''):
        if isinstance(relative_to, int):
            return [v for v in self._tracked_objects.values() if v.v_id != relative_to]
        elif relative_to is '':
            return [v for v in self._tracked_objects.values() if v.v_id != self._vehicle_id]
        elif relative_to is None:
            return self._tracked_objects.values()
        else:
            raise Exception("Case not implemented")

    def get_object(self, v_id):
        assert (type(v_id) is int)
        return self._tracked_objects[v_id]
