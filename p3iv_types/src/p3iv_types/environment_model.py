from __future__ import division
import itertools
from p3iv_types.vehicle import TrackedVehicle


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

    __slots__ = ["_tracked_objects", "_vehicle_id", "polyvision", "visible_areas", "laneletmap"]

    def __init__(self, vehicle_id=None, visible_areas=None, polyvision=None, laneletmap=None):
        self._tracked_objects = {}
        self._vehicle_id = vehicle_id
        self.polyvision = polyvision
        self.visible_areas = visible_areas
        self.laneletmap = laneletmap

    def __getstate__(self):
        """Implement for dump in pickle. Lanelet2 and Polyvision are implemented in C++ and cannot be pickled."""
        delattr(self, "laneletmap")
        delattr(self, "polyvision")

        all_slots = itertools.chain.from_iterable(getattr(t, "__slots__", ()) for t in type(self).__mro__)
        state = {attr: getattr(self, attr) for attr in all_slots if hasattr(self, attr)}
        return state

    def __setstate__(self, state):
        """Implement for load in pickle."""
        for k, v in state.iteritems():
            setattr(self, k, v)

    @property
    def tracked_objects(self):
        return self._tracked_objects

    def add_object(self, v_id, color, length, width, state):
        self._tracked_objects[v_id] = self.create_object(v_id, color, length, width, state)

    @staticmethod
    def create_object(object_id, color, length, width, state):
        tracked_object = TrackedVehicle()
        tracked_object.id = object_id
        tracked_object.color = color
        tracked_object.length = length
        tracked_object.width = width
        tracked_object.state = state
        tracked_object.existence_probability = 1.0
        return tracked_object

    def objects(self, relative_to=""):
        if isinstance(relative_to, int):
            return [v for v in self._tracked_objects.values() if v.id != relative_to]
        elif relative_to is "":
            return [v for v in self._tracked_objects.values() if v.id != self._vehicle_id]
        elif relative_to is None:
            return self._tracked_objects.values()
        else:
            raise Exception("Case not implemented")

    def get_object(self, object_id):
        assert type(object_id) is int
        return self._tracked_objects[object_id]
