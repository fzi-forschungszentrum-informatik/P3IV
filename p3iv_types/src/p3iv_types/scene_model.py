from __future__ import division
import os
import numpy as np
from lanelet2.core import BasicPoint2d
from scene_object import SceneObject
import logging

logger = logging.getLogger(__file__.split(os.path.sep)[-3])
logger.setLevel(logging.DEBUG)


class SceneModel(object):
    """
    Contains information on route, visible regions, and objects in the scene mapped to relative coordinates.

    Attributes
    ----------
    _scene_objects: dict
        dictionary of SceneObjects. Only objects in interaction with ego vehicle are appended to this list.
    position: BasicPoint2d
        Cartesian position of the ego-vehicle. Is used for calculating relative-distances on routing graph.
    laneletsequence: PyLaneletSequence
        LaneletSequence that the vehicle will follow. For ego-vehicle it contains Lanelets that the vehicle has driven.
    visible areas: list
        a list that contains the Cartesian coordinates of visibility polygon
    traffic_rules: TrafficRules
        Traffic rules to obey on this LaneletSequence
    """

    def __init__(self, vehicle_id, position, laneletsequence=None, visible_distances=None):
        self._scene_objects = {}
        self._vehicle_id = vehicle_id
        self.position = BasicPoint2d(position[0], position[1])
        self.laneletsequence = laneletsequence
        self.visible_distances = visible_distances
        self.traffic_rules = None

    def __getstate__(self):
        """Implement for dump in pickle & (indirectly) deepcopy.
        Note that Lanelet2 types cannot be pickled. Pass Lanelet-ids instead, if req.
        """
        d = dict(self.__dict__)
        if "position" in d:
            del d["position"]
        return d

    def __setstate__(self, d):
        """Implement for load in pickle."""
        self.__dict__ = d

    def add_object(
        self, object2add, relative_distance, crossing_begin=-np.inf, crossing_end=np.inf, has_right_of_way=None
    ):
        logger.debug("\x1b[33;21mAdd object into scene-model: %s\x1b[0m" % str(object2add.v_id))

        # align frenet positions with relative position
        offset = object2add.progress - relative_distance
        object2add.progress -= offset

        # crossing begin & end of the input are defined in the coordinate-frame of the object; make them relative to ego
        object2add.crossing_voi_route.begin = object2add.progress + crossing_begin
        object2add.crossing_voi_route.end = object2add.progress + crossing_end

        object2add.has_right_of_way = has_right_of_way

        self.append_object(object2add)

    def append_object(self, scene_object):
        assert isinstance(scene_object, SceneObject)
        self._scene_objects[scene_object.v_id] = scene_object

    @property
    def scene_objects(self):
        return self._scene_objects

    @staticmethod
    def create_object(v_id, color, length, width, state):
        scene_object = SceneObject()
        scene_object.v_id = v_id
        scene_object.color = color
        scene_object.length = length
        scene_object.width = width
        scene_object.state = state
        scene_object.existence_probability = 1.0
        return scene_object

    def objects(self, relative_to=""):
        if isinstance(relative_to, int):
            return [v for v in self._scene_objects.values() if v.v_id != relative_to]
        elif relative_to is "":
            return [v for v in self._scene_objects.values() if v.v_id != self._vehicle_id]
        elif relative_to is None:
            return self._scene_objects.values()
        else:
            raise Exception("Case not implemented")

    def get_object(self, v_id):
        assert type(v_id) is int
        if v_id in self._scene_objects.keys():
            return self._scene_objects[v_id]
        else:
            return None
