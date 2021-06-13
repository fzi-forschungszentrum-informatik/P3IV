from __future__ import division
import os
import itertools
import uuid
import numpy as np
from lanelet2.core import BasicPoint2d
from scipy.interpolate import UnivariateSpline
from scene_object import SceneObject
import logging

logger = logging.getLogger(__file__.split(os.path.sep)[-1])
logger.setLevel(logging.INFO)


class PyLaneletSequence(object):
    """A Python wrapper class for LaneletSequence"""

    def __init__(self, lanelets):
        self._smooth = False
        self._lanelets = lanelets
        self._ids = None
        self._centerline = np.array([]).reshape(-1, 2)
        self._bound_left = np.array([]).reshape(-1, 2)
        self._bound_right = np.array([]).reshape(-1, 2)

    def __getstate__(self):
        """
        Implement for dump in pickle; Lanelet2 is implemented in C++ and cannot be pickled.
        Pass Lanelet-ids instead.
        """
        self.centerline()
        self.bound_right()
        self.bound_left()
        self._lanelets = [ll.id for ll in self.lanelets]
        all_slots = itertools.chain.from_iterable(getattr(t, "__slots__", ()) for t in type(self).__mro__)
        state = {attr: getattr(self, attr) for attr in all_slots if hasattr(self, attr)}
        return state

    @property
    def lanelets(self):
        return self._lanelets

    def centerline(self, smooth=False):
        """
        Get Cartesian coordinates of centerline. Options 'smooth' smoothens zig-zags.
        But, smoothing may sacrifice speed!
        """
        if len(self._centerline) < 1:
            centerline = np.array([self._lanelets[0].centerline[0].x, self._lanelets[0].centerline[0].y])
            for ll in self._lanelets:
                # prevent repeated entries
                for i in range(1, len(ll.centerline)):
                    centerline = np.vstack([centerline, [ll.centerline[i].x, ll.centerline[i].y]])
            self._centerline = centerline

        # if smooth centerline is requested and internally stored one is not smooth
        # (once 'smooth' is set 'True', will always yield smooth centerlines)
        if smooth and not self._smooth:
            self._centerline = self.smooth_centerline(self._centerline)
            self._smooth = True

        return self._centerline

    def bound_left(self):
        """Get the left corridor bound of the laneletsequence."""
        if len(self._bound_left) < 1:
            boundary = np.array([]).reshape(-1, 2)
            for ll in self._lanelets:
                boundary = np.vstack([boundary, [[pt.x, pt.y] for pt in ll.leftBound]])
            self._bound_left = boundary
        return self._bound_left

    def bound_right(self):
        """Get the right corridor bound of the laneletsequence."""
        if len(self._bound_right) < 1:
            boundary = np.array([]).reshape(-1, 2)
            for ll in self._lanelets:
                boundary = np.vstack([boundary, [[pt.x, pt.y] for pt in ll.rightBound]])
            self._bound_right = boundary
        return self._bound_right

    def ids(self):
        """Return IDs of Lanelets in the sequence as a list."""
        if self._ids is None:
            self._ids = [ll.id for ll in self._lanelets]
        return self._ids

    @staticmethod
    def smooth_centerline(centerline, resolution=100):
        """Takes Cartesian coordinates of centerline and smoothens them."""
        distances = np.linalg.norm(np.diff(centerline, axis=0), axis=1)
        distances = np.append(np.array([0]), distances)  # insert 0 to match lengths
        progress = np.cumsum(distances)

        spline_x = UnivariateSpline(progress, centerline[:, 0], k=5)
        spline_y = UnivariateSpline(progress, centerline[:, 1], k=5)
        spline_x.set_smoothing_factor(0.75)
        spline_y.set_smoothing_factor(0.75)
        ps = np.linspace(progress[0], progress[-1], resolution)
        xs = spline_x(ps)
        ys = spline_y(ps)
        return np.asarray(zip(xs, ys))


class RouteOption(object):

    """
    Attributes
    ----------
    uuid: uuid4
        A unique ID for the route option
    laneletsequence: PyLaneletSequence
        LaneletSequence that the vehicle will follow. For ego-vehicle it contains Lanelets that the vehicle has driven.
    """

    __slots__ = ["uuid", "laneletsequence"]

    def __init__(self, laneletsequence_lanelets):
        self.uuid = uuid.uuid4()
        self.laneletsequence = PyLaneletSequence(laneletsequence_lanelets)

    @property
    def lanelets(self):
        return self.laneletsequence.lanelets


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
        object2add.progress = relative_distance
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
