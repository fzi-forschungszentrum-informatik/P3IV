
from enum import Enum
import copy
import numpy as np
import lanelet2
import warnings
import os
import logging
import traceback
from termcolor import colored
from p3iv_types.scene_model import RouteOption, SceneModel
from p3iv_utils.coordinate_transformation import CoordinateTransform
from p3iv_modules.interfaces import SceneUnderstandingInterface
import lanelet2
import lanelet2.matching as lanelet2_matching


# configure logging of the module
logger = logging.getLogger(__file__.split(os.path.sep)[-2])
logger.setLevel(logging.INFO)


class Countries(Enum):
    DEU = 0
    USA = 1
    CHN = 2


class Understand(SceneUnderstandingInterface):
    """
    A class for performing scene understanding.

    Attributes
    ----------
    dt: float
        sampling-time in [ms]
    horizon: float
        planning horizon in [s]
    _laneletmap: Lanelet2-Map
        Lanelet2 map of the current environment
    _traffic_rules: Lanelet2-TrafficRules
        Lanelet2 traffic rules for vehicles
    _routing_graph: Lanelet2-RoutingGraph
        Lanelet2 routing graph to inspect connectivity of lanelets
    _toLanelet: int
        'Lanelet-ID' to which the ego-vehicle is driving. If it is not provided, past tracks including current lanelet
        is taken as reference centerline.
    _route_memory: RouteOption
        RouteOption instance calculated in the timestamp before. Stored as memory to compensate misleading lanelet
        matches in the current timestamp
    """

    def __init__(self, dt, N, laneletmap, ego_vehicle_id, toLanelet=None, *args, **kwargs):
        assert dt > 1
        self.dt = dt / 1000
        self.horizon = N * self.dt
        self._laneletmap = laneletmap
        self._traffic_rules = lanelet2.traffic_rules.create(
            lanelet2.traffic_rules.Locations.Germany, lanelet2.traffic_rules.Participants.Vehicle
        )
        self._routing_graph = lanelet2.routing.RoutingGraph(laneletmap, self._traffic_rules)
        self._id = ego_vehicle_id
        self._toLanelet = toLanelet
        self._route_memory = None

    def __call__(self, tracked_vehicles, *args, **kwargs):
        """
        Run scene understanding given tracked vehicles list.
        Performs visible distance matching if the argument 'polyvision' is provided.

        Parameters
        ----------
        tracked_vehicles: list
            List of TrackedObjects in environment model
        """

        # match tracked_vehicles to lanelets
        scene_objects = []
        for e in tracked_vehicles:

            # match lanelets
            current_lanelets = []
            for m in self.match2Lanelet(self._laneletmap, self._traffic_rules, e.state.pose):
                current_lanelets.append(m.lanelet)

            # create instances of SceneObject
            s = SceneModel.create_object(e.id, e.color, e.length, e.width, e.state)
            s.current_lanelets = current_lanelets

            # append this scene_object to the list
            if e.id == self._id:
                ego_v = s
            else:
                scene_objects.append(s)

        # increase tolerance if no match is found
        if len(ego_v.current_lanelets) == 0:
            current_lanelets = []
            for m in self.match2Lanelet(self._laneletmap, self._traffic_rules, e.state.pose, tolerance=1.0):
                current_lanelets.append(m.lanelet)
            ego_v.current_lanelets = current_lanelets

        for current_llt in ego_v.current_lanelets:
            try:
                # it's not the initial calculation and current lanelet id is in laneletsequence-memory
                if self._route_memory is not None and current_llt.id not in self._route_memory.laneletsequence.ids():
                    continue
                route_to_destination = self._routing_graph.getRoute(
                    current_llt, self._laneletmap.laneletLayer[self._toLanelet]
                )
                lanelet2_laneletsequence = route_to_destination.shortestPath()
                llts = [llt for llt in lanelet2_laneletsequence]
                route_option = RouteOption(llts)
                break
            except AttributeError:
                # if 'toLanelet' is not reachable, lanelet2.python will return 'route_to_destination' as None
                continue
        assert (
            route_option,
            "Lanelet matcher has performed poorly and route option could not be calculated",
        )
        self._route_memory = route_option

        scene_model = SceneModel(ego_v.id, ego_v.state.position.mean, route_option)

        # add only vehicles to the scene model, whose current lanelets are on ego route
        for s in scene_objects:
            for curr_llt in s.current_lanelets:
                if curr_llt.id in route_option.laneletsequence.ids():
                    # calculate Euclidean distance between vehicles
                    v2v_distance = np.linalg.norm(ego_v.state.position.mean - s.state.position.mean)
                    scene_model.add_object(s, v2v_distance)
                    break

        return scene_model

    @staticmethod
    def match2Lanelet(laneletmap, traffic_rules, pose, tolerance=0.0):
        """Use Lanelet2 matching module for matching poses to lanelets"""
        x, y, phi = pose
        o = lanelet2_matching.Object2d()
        o.pose = lanelet2_matching.Pose2d(x, y, np.radians(phi))
        matches_all = lanelet2_matching.getDeterministicMatches(laneletmap, o, tolerance)
        matches = lanelet2_matching.removeNonRuleCompliantMatches(matches_all, traffic_rules)
        return matches
