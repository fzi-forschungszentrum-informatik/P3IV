# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import os
import sys
import logging
import numpy as np
import warnings
import lanelet2
from p3iv_core.bindings.interaction_dataset.track_reader import track_reader
from p3iv_core.bindings.interaction_dataset.data_converter import DataConverter
from p3iv_utils.coordinate_transformation import CoordinateTransform
from p3iv_utils.polygon_operations import PolygonCalculation
from p3iv_types.situation_object import SituationObject
from p3iv_types.maneuvers import ManeuverHypothesis
from p3iv_modules.interfaces import PredictInterface
from p3iv_modules.understanding.basic import Understand
from p3iv_types.situation_model import SituationModel
from p3iv_types.scene_model import RouteOption, SceneModel


logger = logging.getLogger(__file__.split(os.path.sep)[-2])
logger.setLevel(logging.DEBUG)


class Predict(PredictInterface):
    """
    This class reads the true Cartesian values from the dataset and returns these as predicted motion.
    """

    def __init__(self, configurations, laneletmap, *args, **kwargs):
        dt = int(configurations["temporal"]["dt"])
        assert dt > 1
        self._dt = dt
        self._N = int(configurations["temporal"]["N"])
        # todo: update for rounD-based simulation and fallback for custom simulation where no dataset is available
        try:
            self.dataset = DataConverter(configurations)
        except:
            pass
        self._laneletmap = laneletmap
        self._traffic_rules = lanelet2.traffic_rules.create(
            lanelet2.traffic_rules.Locations.Germany, lanelet2.traffic_rules.Participants.Vehicle
        )
        self._routing_graph = lanelet2.routing.RoutingGraph(laneletmap, self._traffic_rules)

    def __call__(self, timestamp, scene_model):
        situation_model = SituationModel()
        for sco in scene_model.objects():
            logger.info(" - predict vehicle-ID :" + str(sco.id))
            sto = self.predict_scene_object(scene_model.route_option, timestamp, sco)
            if not any(sto.maneuvers.hypotheses[0].overlap):
                # clear object from scene model
                del scene_model._scene_objects[sto.id]
                continue
            situation_model.add(sto)
        return situation_model

    def predict_scene_object(self, route_option, timestamp, scene_object):
        """Create a SituationObject filled with ground-truth-prediction."""
        situation_object = SituationObject(scene_object)
        pose_array = self.read_pose(timestamp, situation_object.id)
        goal_candidates = self.read_goal_lanelet(situation_object.id)

        try:
            # if SceneModel(s) are extracted for SceneObjects in understanding module
            route_scene, overlap = self.get_maneuver_path(route_option, scene_object, pose_array)
        except AssertionError:
            # Routes will be extracted for SceneObjects with the help of lanelet matcher
            route_scene, overlap = self.create_maneuver_path(route_option, scene_object, pose_array, goal_candidates)

        pose_array = self.fix_zeros(pose_array, route_scene.route_option.laneletsequence.centerline(), self._dt)
        self.create_maneuvers(scene_object, situation_object, route_scene, overlap)
        self.set_motion_components(situation_object.maneuvers.hypotheses[0], pose_array, scene_object)
        return situation_object

    def read_pose(self, timestamp, vehicle_id):
        """Read poses from dataset as numpy array"""

        for t_id in list(self.dataset.tracks.keys()):

            if t_id == vehicle_id:
                pose_array = np.zeros([(self._N + 1), 3])

                timestamps_until_horizon = np.arange(timestamp, timestamp + self._N * self._dt + 1, self._dt)
                for i, ts in enumerate(timestamps_until_horizon):
                    try:
                        data = self.dataset.read_track_at_timestamp(t_id, ts)
                        pose_array[i] = data[1:4]
                    # data is not available for the full horizon
                    except Exception as e:
                        # print(e)
                        break
                break
        return pose_array

    def read_goal_lanelet(self, vehicle_id):
        """
        Read destination Lanelet ID from dataset
        """
        if vehicle_id in list(self.dataset.tracks.keys()):
            # read the last track for the vehicle
            if sys.version_info[0] == 3:
                last_motion_state = list(self.dataset.tracks[vehicle_id].motion_states.values())[-1]
            else:
                # .values() in Python2 will yield unordered list
                last_timestamp = max(self.dataset.tracks[vehicle_id].motion_states.keys())
                last_motion_state = self.dataset.tracks[vehicle_id].motion_states[last_timestamp]

            x, y, yaw_degrees = last_motion_state.x, last_motion_state.y, np.rad2deg(last_motion_state.psi_rad)

            # vehicles sometimes leave their lane; add tolerance of 2 meters
            current_matches = Understand.match2Lanelet(
                self._laneletmap, self._traffic_rules, [x, y, yaw_degrees], tolerance=2.0
            )

            # there may be multiple candidates; return all of them
            goal_candidates = [match.lanelet for match in current_matches]
            return goal_candidates
        else:
            raise KeyError("Vehicle not in track dictionary")

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
                speed = np.linalg.norm(displacement) / (dt / 1000.0)
                arc_pos = c.xy2ld(pose_array[i - 1][:2])[0] + speed * dt / 1000.0
                try:
                    # if arc_pos is longer than centerline, IndexError will be raised
                    x, y = c.ld2xy([arc_pos, 0])
                    yaw = np.degrees(np.arctan2(displacement[1], displacement[0]))
                    pose_array[i] = np.asarray([x, y, yaw])
                except IndexError:
                    pose_array[i] = pose_array[i - 1]
        return pose_array

    def get_maneuver_path(self, route_option, scene_object, pose_array):
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
        return rso, None

    def create_maneuver_path(self, route_option, scene_object, pose_array, goal_candidates):

        # find unique lanelet matches
        i = 0
        llt_matches_list = []
        overlap = []
        while i < len(pose_array):
            # get all lanelet matches for current pose
            current_matches = Understand.match2Lanelet(
                self._laneletmap, self._traffic_rules, pose_array[i], tolerance=2.0
            )

            # if any current match is on route-option lanelets of ego (host) vehicle fill overlap list with True
            current_match_ids = [cm.lanelet.id for cm in current_matches]
            if any((True for x in current_match_ids if x in route_option.laneletsequence.ids())):
                overlap.append(True)
            else:
                overlap.append(False)

            # if the current lanelet matches is new, append this to the match list
            if len(llt_matches_list) == 0 or not lanelet_matches_equal(current_matches, llt_matches_list[-1]):
                llt_matches_list.append(current_matches)
            i += 1

        # get the first matches from matches_list and check if any leads to destination
        route_alternatives = []
        for goal_lanelet in goal_candidates:
            for match in llt_matches_list[0]:
                try:
                    # use routing graph
                    lanelet2sequence = self._routing_graph.getRoute(match.lanelet, goal_lanelet).shortestPath()

                    # add to candidates
                    route_option = RouteOption([llt for llt in lanelet2sequence])
                    route_alternatives.append(route_option)
                except:
                    pass

        # get the shortest route
        if sys.version_info[0] == 3:
            route_option = min(route_alternatives, key=lambda r: r.laneletsequence.length)
        else:
            route_lengths = [r.laneletsequence.length for r in route_alternatives]
            route_option = route_alternatives[route_lengths.index(min(route_lengths))]

        route_scene = SceneModel(scene_object.id, scene_object.state.position.mean, route_option)
        return route_scene, overlap

    def create_maneuvers(self, scene_object, situation_object, pso, overlap):
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
                self._dt * self._N * 1000.0,
            )
        ]
        # set only those which are read form dataset
        # (fix_zeros adds virtual entries. These do not overlap.
        # Hence, default value of 'False' is left untouched).
        for i, o in enumerate(overlap):
            hypotheses[0].overlap[i] = o
        hypotheses[0].probability.route = 1.0
        hypotheses[0].probability.maneuver = 1.0
        situation_object.maneuvers.add(hypotheses)

    def set_motion_components(self, maneuver_hypothesis, pose_array, scene_object):
        """Calculate velocity etc. in Cartesian frame & Frenet motion"""
        c = CoordinateTransform(maneuver_hypothesis.path.centerline())
        maneuver_hypothesis.motion(pose_array[:, :2], dt=self._dt)
        pos_arc = c.xy2ld(maneuver_hypothesis.motion.position.mean)
        offset = pos_arc[0, 0] - scene_object.progress
        pos_arc[:, 0] -= offset

        # if vehicle is in oncoming direction
        if scene_object.speed_sign < 0:
            pos_arc[1:, 0] = pos_arc[0, 0] - np.diff(pos_arc[:, 0]) / (self._dt * 1000.0)

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
