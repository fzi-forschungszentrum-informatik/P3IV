from __future__ import division
import os
import itertools
import numpy as np
from lanelet2.core import BasicPoint2d
from scene_object import SceneObject
import logging

logger = logging.getLogger(__file__.split(os.path.sep)[-1])
logger.setLevel(logging.INFO)


class SceneModel(object):
    """
    Contains information on route, visible regions, and objects in the scene mapped to relative coordinates.
    For every route option there is a SceneModel.

    Attributes
    ----------
    _object_id: int
        ID of the object which a scene model is built
    _scene_objects: dict
        Dictionary of SceneObjects. Only objects in interaction with ego vehicle are appended to this list.
    position: BasicPoint2d
        Cartesian position of the ego-vehicle. Is used for calculating relative-distances on routing graph.
    route_option: RouteOption
        Route option for which as scene model is built
    visible_distances: list
        a list that contains the Cartesian coordinates of visibility polygon
    """

    __slots__ = [
        "_object_id",
        "_scene_objects",
        "position",
        "route_option",
        "visible_distances",
    ]

    def __init__(self, object_id, position, route_option, visible_distances=None):
        self._object_id = object_id
        self._scene_objects = {}
        self.position = BasicPoint2d(position[0], position[1])
        self.route_option = route_option
        self.visible_distances = visible_distances

    def __getstate__(self):
        """Implement for dump in pickle & (indirectly) deepcopy.
        Note that Lanelet2 types, such as 'position' cannot be pickled as they are boost-python instances.
        """
        all_slots = itertools.chain.from_iterable(getattr(t, "__slots__", ()) for t in type(self).__mro__)
        state = {attr: getattr(self, attr) for attr in all_slots if hasattr(self, attr) and attr != "position"}
        return state

    def __setstate__(self, state):
        """Implement for load in pickle."""
        for k, v in state.iteritems():
            setattr(self, k, v)

    def add_object(self, object2add, relative_distance):
        logger.debug(
            "\x1b[33;24mAdd object into scene-model #%s: %s\x1b[0m" % (str(self._object_id), str(object2add.id))
        )

        # align frenet positions with relative position
        offset = object2add.progress - relative_distance
        object2add.progress -= offset
        self.append_object(object2add)

    def append_object(self, scene_object):
        assert isinstance(scene_object, SceneObject)
        self._scene_objects[scene_object.id] = scene_object

    @property
    def scene_objects(self):
        return self._scene_objects

    @staticmethod
    def create_object(object_id, color, length, width, state):
        scene_object = SceneObject()
        scene_object.id = object_id
        scene_object.color = color
        scene_object.length = length
        scene_object.width = width
        scene_object.state = state
        scene_object.existence_probability = 1.0
        return scene_object

    def objects(self, relative_to=""):
        if isinstance(relative_to, int):
            return [v for v in self._scene_objects.values() if v.id != relative_to]
        elif relative_to is "":
            return [v for v in self._scene_objects.values() if v.id != self._object_id]
        elif relative_to is None:
            return self._scene_objects.values()
        else:
            raise Exception("Case not implemented")

    def get_object(self, object_id):
        assert type(object_id) is int
        if object_id in self._scene_objects.keys():
            return self._scene_objects[object_id]
        else:
            return None
