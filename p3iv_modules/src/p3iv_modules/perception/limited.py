import numpy as np
import warnings
from p3iv_modules.perception.perfect import Percept as PerfectPerception
from p3iv_modules.interfaces.perception import PerceptInterface
from p3iv_types.environment_model import EnvironmentModel
from p3iv_utils.vehicle_rectangle import VehicleRectangle
from p3iv_utils_polyvision.fov_wedge import generateFoVWedge
from p3iv_utils_polyvision_pyapi.pypolyvision import VisibleArea, checkInside


class VisibilityModel(object):
    def __init__(self, sensors):
        self._sensors = sensors
        self._field_of_view = None
        self.polyvision = None  # instance of cpp visibility calculator
        self._visible_areas = None
        self._opaque_polygons = None
        self._non_visible_areas = None

    def __call__(self, origin, heading, obstacle_polygons):
        allFieldOfView = []
        for fov in self._sensors:
            allFieldOfView.append(
                generateFoVWedge(fov.begin, fov.end, fov.range, heading=heading, origin=np.asarray(origin))
            )
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
                    gt_o.timestamps.latest().state.position.mean, list(self._field_of_view[0])
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
    def __init__(
        self,
        ego_v_id,
        per_pos_sigma_x,
        per_pos_sigma_y,
        per_pos_cross_corr,
        per_vel_sigma_x,
        per_vel_sigma_y,
        per_vel_cross_corr,
        loc_pos_sigma_x,
        loc_pos_sigma_y,
        loc_pos_cross_corr,
        loc_vel_sigma_x,
        loc_vel_sigma_y,
        loc_vel_cross_corr,
        laneletmap,
        sensors,
    ):
        """
        Parameters
        ----------
        Check PerceptInterface abstract class
        """

        self._ego_v_id = ego_v_id

        # position covariance matrix for percepted objects
        self.per_pos_cov = np.asarray(
            [
                [per_pos_sigma_x ** 2, per_pos_cross_corr * per_pos_sigma_x * per_pos_sigma_y],
                [per_pos_cross_corr * per_pos_sigma_x * per_pos_sigma_y, per_pos_sigma_y ** 2],
            ]
        )
        # velocity covariance matrix for percepted objects
        self.per_vel_cov = np.asarray(
            [
                [per_vel_sigma_x ** 2, per_vel_cross_corr * per_vel_sigma_x * per_vel_sigma_y],
                [per_vel_cross_corr * per_vel_sigma_x * per_vel_sigma_y, per_vel_sigma_y ** 2],
            ]
        )
        # position covariance matrix for localization - ego vehicle
        self.loc_pos_cov = np.asarray(
            [
                [loc_pos_sigma_x ** 2, loc_pos_cross_corr * loc_pos_sigma_x * loc_pos_sigma_y],
                [loc_pos_cross_corr * loc_pos_sigma_x * loc_pos_sigma_y, loc_pos_sigma_y ** 2],
            ]
        )
        # velocity covariance matrix for localization - ego vehicle
        self.loc_vel_cov = np.asarray(
            [
                [loc_vel_sigma_x ** 2, loc_vel_cross_corr * loc_vel_sigma_x * loc_vel_sigma_y],
                [loc_vel_cross_corr * loc_vel_sigma_x * loc_vel_sigma_y, loc_vel_sigma_y ** 2],
            ]
        )

        self._laneletmap = laneletmap
        self._visibility_model = VisibilityModel(sensors)
        self._visibility_model2plot = VisibilityModel(sensors)

        self._polygons_static = self._get_static_obstacle_polygons(laneletmap)
        # self._measurement_model = ImperfectMeasurement(self.ego_id, self.ego_route, self.roads, sensor_range, perception_noise)

    def __call__(self, timestamp, ground_truth, pose, *args, **kwargs):
        x, y, current_yaw_angle = pose
        current_cartesian_pos = np.asarray([x, y])
        gt_list = PerfectPerception.get_ground_truth_timestamp(timestamp, ground_truth)

        obstacle_polygons = self._get_dynamic_obstacle_polygons(gt_list) + self._polygons_static
        self._visibility_model2plot(current_cartesian_pos, current_yaw_angle, obstacle_polygons)
        warnings.warn("implement static and dynamic object polygons")
        obstacle_polygons = []
        self._visibility_model(current_cartesian_pos, current_yaw_angle, obstacle_polygons)
        percepted_objects = self._visibility_model.get_percepted_objects(gt_list, self._ego_v_id)

        environment_model = EnvironmentModel(
            vehicle_id=self._ego_v_id,
            visible_areas=self._visibility_model2plot.visible_areas,
            polyvision=self._visibility_model.polyvision,
        )
        # environment_model.visible_areas2plot = self._visibility_model2plot.visible_areas

        PerfectPerception.fill_environment_model(
            self._ego_v_id,
            environment_model,
            ground_truth,
            percepted_objects,
            self.per_pos_cov,
            self.per_vel_cov,
            self.loc_pos_cov,
            self.loc_vel_cov,
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
                    v.timestamps.latest().state.yaw.mean + 90,
                )
                corner_points.append(c)
        return corner_points
