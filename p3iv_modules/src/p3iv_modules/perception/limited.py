from __future__ import absolute_import, division
import numpy as np
import warnings
from p3iv_modules.perception.perfect import Percept as PerfectPerception
from p3iv_modules.interfaces.perception import PerceptInterface
from p3iv_types.environment_model import EnvironmentModel
from p3iv_utils.vehicle_rectangle import VehicleRectangle
from polyvision.fov_wedge import generateFoVWedge
from polyvision_pyapi.pypolyvision import VisibleArea, checkInside


class VisibilityModel(object):
    def __init__(self, field_of_views):
        self._field_of_views = field_of_views
        self._field_of_view = None
        self.polyvision = None  # instance of cpp visibility calculator
        self._visible_areas = None
        self._opaque_polygons = None
        self._non_visible_areas = None

    def __call__(self, origin, heading, obstacle_polygons):
        allFieldOfView = []
        for fov_props in self._field_of_views:
            v_angle = fov_props[0]
            v_range = fov_props[1]
            allFieldOfView.append(generateFoVWedge(v_angle, v_range, directionAngle=heading, origin=np.asarray(origin)))
        self.polyvision = VisibleArea(origin, allFieldOfView, obstacle_polygons)
        self.polyvision.calculateVisibleArea()

        self._field_of_view = self.polyvision.getFieldsOfView()
        self._visible_areas = self._close_polygons(self.polyvision.getVisibleAreas())
        self._opaque_polygons = self.polyvision.getOpaquePolygons()
        self._non_visible_areas = self.polyvision.getNonVisibleAreas()

    def get_percepted_objects(self, ground_truth_objects, ego_v_id):
        if not self._visible_areas:
            return []
        else:
            percepted_objects = []
            for gt_o in ground_truth_objects:
                if gt_o.id != ego_v_id and checkInside(
                    gt_o.timestamps.latest().state.position.mean, [self._field_of_view]
                ):
                    percepted_objects.append(gt_o)
            return percepted_objects

    @property
    def field_of_view(self):
        return self._field_of_view

    @property
    def visible_areas(self):
        return self._visible_areas

    @property
    def opaque_polygons(self):
        return self._opaque_polygons

    @property
    def non_visible_areas(self):
        return self._non_visible_areas

    @staticmethod
    def _close_polygons(polygons):
        visible_areas = []
        for va_ in polygons:
            va_ = np.vstack([va_, va_[0]])
            visible_areas.append(va_)
        return visible_areas


class Percept(PerceptInterface):
    def __init__(self, ego_v_id, laneletmap, sensor_fov, sensor_range, sensor_noise):
        self._ego_v_id = ego_v_id
        self._laneletmap = laneletmap
        fovs = [(sensor_fov, sensor_range)]
        self._visibility_model = VisibilityModel(fovs)
        # self._visibility_model2plot = VisibilityModel(fovs)

        self._polygons_static = self._get_static_obstacle_polygons(laneletmap)
        # self._measurement_model = ImperfectMeasurement(self.ego_id, self.ego_route, self.roads, sensor_range, perception_noise)

    def __call__(self, timestamp, ground_truth, pose, *args, **kwargs):
        x, y, current_yaw_angle = pose
        current_cartesian_pos = np.asarray([x, y])
        gt_list = PerfectPerception.get_ground_truth_timestamp(timestamp, ground_truth)

        obstacle_polygons = self._get_dynamic_obstacle_polygons(gt_list) + self._polygons_static
        # self._visibility_model2plot(current_cartesian_pos, current_yaw_angle, obstacle_polygons)
        warnings.warn("implement static and dynamic object polygons")
        obstacle_polygons = []
        self._visibility_model(current_cartesian_pos, current_yaw_angle, obstacle_polygons)
        percepted_objects = self._visibility_model.get_percepted_objects(gt_list, self._ego_v_id)

        environment_model = EnvironmentModel(
            vehicle_id=self._ego_v_id,
            visible_areas=self._visibility_model.visible_areas,
            polyvision=self._visibility_model.polyvision,
        )
        # environment_model.visible_areas2plot = self._visibility_model2plot.visible_areas
        for po in percepted_objects:
            environment_model.add_object(
                po.id, po.appearance.color, po.appearance.length, po.appearance.width, po.timestamps.latest().state
            )

        environment_model.add_object(
            ground_truth[self._ego_v_id].id,
            ground_truth[self._ego_v_id].appearance.color,
            ground_truth[self._ego_v_id].appearance.length,
            ground_truth[self._ego_v_id].appearance.width,
            ground_truth[self._ego_v_id].timestamps.latest().state,
        )

        return environment_model

    @staticmethod
    def _get_static_obstacle_polygons(ground_truth_value):
        """
        buildings_as_polygons = []
        for _, building in buildings.iteritems():
            buildings_as_polygons.append(Polygon(np.asarray(building.nodes[:-1])))  # first and last node are the same
        """
        return []

    def _get_dynamic_obstacle_polygons(self, ground_truth_objects):
        """Calculate the polygons of vehicle corner points"""
        corner_points = []
        for v in ground_truth_objects:
            if v.id != self._ego_v_id:
                c = VehicleRectangle.get_corners(
                    v.appearance.length,
                    v.appearance.width,
                    v.timestamps.latest().state.position.mean,
                    v.timestamps.latest().state.yaw.mean,
                )
                corner_points.append(c)
        return corner_points