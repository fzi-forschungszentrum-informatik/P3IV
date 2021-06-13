from __future__ import division, absolute_import
import os
import logging
import numpy as np
import warnings
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import lanelet2
from p3iv_core.bindings.interaction_dataset.track_reader import track_reader
from p3iv_core.bindings.interaction_dataset.data_converter import DataConverter
from p3iv_utils.coordinate_transformation import CoordinateTransform
from p3iv_types.situation_object import SituationObject
from p3iv_types.maneuvers import ManeuverHypothesis
from p3iv_modules.interfaces import PredictInterface
from p3iv_modules.understanding.basic import Understand
from p3iv_types.situation_model import SituationModel
from p3iv_types.scene_model import RouteOption, SceneModel


logger = logging.getLogger(__file__.split(os.path.sep)[-2])
logger.setLevel(logging.DEBUG)


class Prediction(PredictInterface):
    """
    This class reads the true Cartesian values from the dataset and returns these as predicted motion.
    """

    def __init__(self, dt, N, map_name, prediction_configs, interaction_dataset_dir, laneletmap, *args, **kwargs):
        assert dt > 1
        self._dt = dt
        self._N = N
        self.track_dictionary = track_reader(map_name, interaction_dataset_dir)
        self.dataset_handler = DataConverter(int(self._dt), self.track_dictionary)
        self._laneletmap = laneletmap
        self._traffic_rules = lanelet2.traffic_rules.create(
            lanelet2.traffic_rules.Locations.Germany, lanelet2.traffic_rules.Participants.Vehicle
        )
        self._routing_graph = lanelet2.routing.RoutingGraph(laneletmap, self._traffic_rules)

    def __call__(self, timestamp, scene_model):
        situation_model = SituationModel()
        for sco in scene_model.objects():
            logger.info(" - predict vehicle-ID :" + str(sco.id))
            sto = self.predict_scene_object(timestamp, sco)
            situation_model.add(sto)
        return situation_model

    def predict_scene_object(self, timestamp, scene_object):
        """Create a SituationObject filled with ground-truth-prediction."""
        situation_object = SituationObject(scene_object)
        pose_array = self.read_pose(timestamp, situation_object.id)

        try:
            # if SceneModel(s) are extracted for SceneObjects in understanding module
            rso = self.get_maneuver_path(scene_object, situation_object, pose_array)
        except AssertionError:
            # Routes will be extracted for SceneObjects with the help of lanelet matcher
            rso = self.create_maneuver_path(scene_object, situation_object, pose_array)

        pose_array = self.fix_zeros(pose_array, rso.route_option.laneletsequence.centerline(), self._dt)
        self.create_maneuvers(scene_object, situation_object, rso)
        self.set_motion_components(situation_object.maneuvers.hypotheses[0], pose_array, scene_object.progress)
        return situation_object

    def read_pose(self, timestamp, vehicle_id):
        """Read poses from dataset as numpy array"""

        for t_id in self.track_dictionary.keys():

            if t_id == vehicle_id:
                pose_array = np.zeros([(self._N + 1), 3])

                timestamps_until_horizon = np.arange(timestamp, timestamp + self._N * self._dt + 1, self._dt)
                for i, ts in enumerate(timestamps_until_horizon):
                    try:
                        data = self.dataset_handler.read_track_at_timestamp(t_id, ts)
                        pose_array[i] = data[1:4]
                    # data is not available for the full horizon
                    except Exception as e:
                        # print e
                        break
                break
        return pose_array

    @staticmethod
    def fix_zeros(pose_array, centerline, dt):
        """
        Replace zeros with either extrapolated values or if the reference centerline ends,
        with the latest available value"""

        c = CoordinateTransform(centerline)
        for i, pose in enumerate(pose_array):
            if np.sum(pose[:2]) == 0:
                # assert (i > 1)
                displacement = pose_array[i - 1][:2] - pose_array[i - 2][:2]
                speed = np.linalg.norm(displacement) / (dt / 1000)
                arc_pos = c.xy2ld(pose_array[i - 1][:2])[0] + speed * dt / 1000
                try:
                    # if arc_pos is longer than centerline, IndexError will be raised
                    x, y = c.ld2xy([arc_pos, 0])
                    yaw = np.degrees(np.arctan2(displacement[1], displacement[0]))
                    pose_array[i] = np.asarray([x, y, yaw])
                except IndexError:
                    pose_array[i] = pose_array[i - 1]
        return pose_array

    def get_maneuver_path(self, scene_object, situation_object, pose_array):
        """Among many route options, pick the one that matches with the ground-truth."""

        assert len(scene_object.route_scenes) > 0

        for non_zero_length, pose in enumerate(pose_array):
            if np.sum(pose) == 0:
                break

        for rso in scene_object.route_scenes:
            # evaluate all; match with
            pc = PolygonCalculation(
                rso.route_option.laneletsequence.bound_right(), rso.route_option.laneletsequence.bound_left()
            )
            for xy in pose_array[:non_zero_length, :2]:
                if not pc(xy):
                    break
            else:
                break
        return rso

    def create_maneuver_path(self, scene_object, situation_object, pose_array):

        # find unique lanelet matches
        i = 0
        llt_matches_list = []
        while i < len(pose_array):
            current_matches = Understand.match2Lanelet(self._laneletmap, self._traffic_rules, pose_array[i])
            if len(llt_matches_list) == 0 or not lanelet_matches_equal(current_matches, llt_matches_list[-1]):
                llt_matches_list.append(current_matches)
            i += 1

        # convert the list of lanelet-matches to a list of matched lanelets
        matched_llts = []
        for llt_matches in llt_matches_list:
            if len(llt_matches) != 0:
                matched_llts.append([llms.lanelet for llms in llt_matches])

        # remove not-connected matches from the list
        for j in range(1, len(matched_llts) - 1):
            current_llt_ids = [cllt.id for cllt in matched_llts[j]]
            following_ids = self._allLaneletsConnectedWithCurrentLaneletsFollowing(matched_llts[j], current_llt_ids)
            for m in matched_llts[j + 1]:
                if m.id not in following_ids:
                    matched_llts[j + 1].remove(m)

            current_llt_ids = [cllt.id for cllt in matched_llts[j]]
            previous_ids = self._allLaneletsConnectedWithCurrentLaneletsPrevious(matched_llts[j], current_llt_ids)
            for m in matched_llts[j - 1]:
                if m.id not in previous_ids:
                    matched_llts[j - 1].remove(m)

        try:
            # use routing graph
            lanelet2sequence = self._routing_graph.getRoute(matched_llts[0][0], matched_llts[-1][0]).shortestPath()
            route_lanelets = [llt for llt in lanelet2sequence]
        except:
            # use lanelet matches - eleminate subsequently occuring multiple same lanelet matches
            # e.g. [30032, 30016, 30016, 30016, 30017, 30017, 30017, 30036, ...]
            route_lanelets = []
            latest_llt_id = None
            for llt_matches in matched_llts:
                llt_m = llt_matches[0]
                if llt_m.id != latest_llt_id:
                    route_lanelets.append(llt_m)
                    latest_llt_id = llt_m.id

        route_option = RouteOption(route_lanelets)
        rso = SceneModel(scene_object.id, scene_object.state.position.mean, route_option)
        return rso

    def create_maneuvers(self, scene_object, situation_object, pso):
        """
        Create a single ManeuverHypothesis that matches the ground-truth trajectory.
        Add the ManeuverHypothesis in situation_object.
        """
        speed_limit = [self._traffic_rules.speedLimit(pso.route_option.laneletsequence.lanelets[0]).speedLimit]

        hypotheses = [
            ManeuverHypothesis(
                scene_object.state,
                scene_object.progress,
                pso.route_option.laneletsequence,
                speed_limit,
                self._dt,
                self._N,
                self._dt * self._N * 1000,
            )
        ]
        hypotheses[0].probability.route = 1.0
        hypotheses[0].probability.maneuver = 1.0
        situation_object.maneuvers.add(hypotheses)

    def set_motion_components(self, maneuver_hypothesis, pose_array, progress):
        """Calculate velocity etc. in Cartesian frame & Frenet motion"""
        c = CoordinateTransform(maneuver_hypothesis.path.centerline())
        maneuver_hypothesis.motion(pose_array[:, :2], dt=self._dt)
        pos_arc = c.xy2ld(maneuver_hypothesis.motion.position.mean)
        offset = pos_arc[0, 0] - progress
        pos_arc[:, 0] -= offset
        maneuver_hypothesis.progress = pos_arc

    def _allLaneletsConnectedWithCurrentLaneletsFollowing(self, current_llts, current_llt_ids):
        """Get all lanelets connected to the current lanelet."""
        reachable_ids = set(current_llt_ids)
        for cllt in current_llts:
            for fl in self._routing_graph.following(cllt):
                reachable_ids.add(fl.id)
        return list(reachable_ids)

    def _allLaneletsConnectedWithCurrentLaneletsPrevious(self, current_llts, current_llt_ids):
        """Get all lanelets connected to the current lanelet."""
        reachable_ids = set(current_llt_ids)
        for cllt in current_llts:
            for fl in self._routing_graph.previous(cllt):
                reachable_ids.add(fl.id)
        return list(reachable_ids)


def lanelet_matches_equal(match1, match2):
    match1_ids = [m.lanelet.id for m in match1]
    match2_ids = [m.lanelet.id for m in match2]
    return match1_ids == match2_ids


class PolygonCalculation(object):
    def __init__(self, right_bound, left_bound):
        """Create a shapely-polygon"""
        p = np.vstack([right_bound, left_bound[::-1]])
        self.polygon = Polygon(p)

    def __call__(self, point_xy):
        """Check if point is inside polygon. Return boolean"""
        point = Point(point_xy[0], point_xy[1])
        return self.polygon.contains(point)
