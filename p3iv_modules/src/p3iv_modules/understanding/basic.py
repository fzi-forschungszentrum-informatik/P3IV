from __future__ import division, absolute_import
from enum import Enum
import copy
import numpy as np
import lanelet2
import warnings
import os
import logging
import traceback
import time
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
    """

    def __init__(self, dt, N, laneletmap, ego_vehicle_id, toLanelet=None):
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

    def __call__(self, tracked_vehicles, *args, **kwargs):
        """
        Run scene understanding given tracked vehicles list.
        Performs visible distance matching if the argument 'polyvision' is provided.

        Parameters
        ----------
        tracked_vehicles: list
            List of TrackedObjects in environment model
        """
        ts = time.time()

        # match tracked_vehicles to lanelets
        scene_objects = []
        for e in tracked_vehicles:

            # match lanelets
            x, y, phi = e.state.pose
            o = lanelet2_matching.Object2d()
            o.pose = lanelet2_matching.Pose2d(x, y, np.radians(phi))
            tolerance = 0.0
            matches_all = lanelet2_matching.getDeterministicMatches(self._laneletmap, o, tolerance)
            matches = lanelet2_matching.removeNonRuleCompliantMatches(matches_all, self._traffic_rules)
            current_lanelets = []
            for m in matches:
                current_lanelets.append(m.lanelet)

            # create instances of SceneObject
            s = SceneModel.create_object(e.id, e.color, e.length, e.width, e.state)
            s.current_lanelets = current_lanelets

            # append this scene_object to the list
            if e.id == self._id:
                ego_v = s
            else:
                scene_objects.append(s)

        for current_llt in ego_v.current_lanelets:
            try:
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

        scene_model = SceneModel(ego_v.id, ego_v.state.position.mean, route_option)

        for s in scene_objects:
            scene_model.add_object(s, 0.0)

        print(time.time() - ts)
        return scene_model
