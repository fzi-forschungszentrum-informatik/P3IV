from __future__ import division, absolute_import
import os
import logging
import numpy as np
import warnings
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from p3iv_core.bindings.interaction_dataset.track_reader import track_reader
from p3iv_core.bindings.interaction_dataset.data_converter import DataConverter
from p3iv_utils.coordinate_transformation import CoordinateTransform
from p3iv_types.situation_object import SituationObject
from p3iv_types.maneuvers import ManeuverHypothesis
from p3iv_modules.interfaces import PredictInterface
from p3iv_types.situation_model import SituationModel


logger = logging.getLogger(__file__.split(os.path.sep)[-2])
logger.setLevel(logging.DEBUG)


class Prediction(PredictInterface):
    """
    This class reads the true Cartesian values from the dataset and returns these as predicted motion.
    """

    def __init__(self, dt, N, map_name, prediction_configs, interaction_dataset_dir, *args, **kwargs):
        assert dt > 1
        self._dt = dt
        self._N = N
        self.track_dictionary = track_reader(map_name, interaction_dataset_dir)
        self.dataset_handler = DataConverter(int(self._dt), self.track_dictionary)

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
        xys, yaws = self.read_pose(timestamp, situation_object.id)
        rso = self.get_maneuver_path(scene_object, situation_object, xys, yaws)
        xys, yaws = self.fix_zeros(xys, yaws, rso.route_option.laneletsequence.centerline(), self._dt)
        self.create_maneuvers(scene_object, situation_object, rso)
        self.set_motion_components(situation_object.maneuvers.hypotheses[0], xys, yaws, scene_object.progress)
        return situation_object

    def read_pose(self, timestamp, vehicle_id):
        """Read poses from dataset as numpy array"""

        for t_id in self.track_dictionary.keys():

            if t_id == vehicle_id:
                xys = np.zeros([(self._N + 1), 2])
                yaws = np.zeros([(self._N + 1)])

                timestamps_until_horizon = np.arange(timestamp, timestamp + self._N * self._dt + 1, self._dt)
                for i, ts in enumerate(timestamps_until_horizon):
                    try:
                        data = self.dataset_handler.read_track_at_timestamp(t_id, ts)
                        xys[i] = data[1:3]
                        yaws[i] = data[3]
                    # data is not available for the full horizon
                    except Exception as e:
                        # print e
                        break
                break
        return xys, yaws

    @staticmethod
    def fix_zeros(xys, yaws, centerline, dt):
        """
        Replace zeros with either extrapolated values or if the reference centerline ends,
        with the latest available value"""
        assert len(xys) == len(yaws)

        c = CoordinateTransform(centerline)
        for i, xy in enumerate(xys):
            if np.sum(xy) == 0:
                # assert (i > 1)
                displacement = xys[i - 1] - xys[i - 2]
                speed = np.linalg.norm(displacement) / (dt / 1000)
                arc_pos = c.xy2ld(xys[i - 1])[0] + speed * dt / 1000
                try:
                    # if arc_pos is longer than centerline, IndexError will be raised
                    xys[i] = c.ld2xy([arc_pos, 0])
                    yaws[i] = np.degrees(np.arctan2(displacement[1], displacement[0]))
                except IndexError:
                    xys[i] = xys[i - 1]
                    yaws[i] = yaws[i - 1]
        return xys, yaws

    def get_maneuver_path(self, scene_object, situation_object, xys, yaws):
        """Among many route options, pick the one that matches with the ground-truth."""

        assert len(scene_object.route_scenes) > 0

        for non_zero_length, xy in enumerate(xys):
            if np.sum(xy) == 0:
                break

        for rso in scene_object.route_scenes:
            # evaluate all; match with
            pc = PolygonCalculation(
                rso.route_option.laneletsequence.bound_right(), rso.route_option.laneletsequence.bound_left()
            )
            for xy in xys[:non_zero_length]:
                if not pc(xy):
                    break
            else:
                break
        return rso

    def create_maneuvers(self, scene_object, situation_object, pso):
        """
        Create a single ManeuverHypothesis that matches the ground-truth trajectory.
        Add the ManeuverHypothesis in situation_object.
        """

        hypotheses = [
            ManeuverHypothesis(
                scene_object.state,
                scene_object.progress,
                pso.route_option.laneletsequence,
                pso.route_option.traffic_rules.speed_limits,
                self._dt,
                self._N,
                self._dt * self._N * 1000,
            )
        ]
        hypotheses[0].probability.route = 1.0
        hypotheses[0].probability.maneuver = 1.0
        situation_object.maneuvers.add(hypotheses)

    def set_motion_components(self, maneuver_hypothesis, xys, yaws, progress):
        """Calculate velocity etc. in Cartesian frame & Frenet motion"""
        c = CoordinateTransform(maneuver_hypothesis.path.centerline())
        maneuver_hypothesis.motion(xys, dt=self._dt)
        pos_arc = c.xy2ld(maneuver_hypothesis.motion.position.mean)
        pos_arc[:, 0] += progress
        maneuver_hypothesis.progress = pos_arc


class PolygonCalculation(object):
    def __init__(self, right_bound, left_bound):
        """Create a shapely-polygon"""
        p = np.vstack([right_bound, left_bound[::-1]])
        self.polygon = Polygon(p)

    def __call__(self, point_xy):
        """Check if point is inside polygon. Return boolean"""
        point = Point(point_xy[0], point_xy[1])
        return self.polygon.contains(point)
