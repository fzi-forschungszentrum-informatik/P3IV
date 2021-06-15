
import numpy as np
from p3iv_modules.interfaces.perception import PerceptInterface
from p3iv_types.environment_model import EnvironmentModel


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
        *args,
        **kwargs
    ):
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

    def __call__(self, timestamp, ground_truth, *args, **kwargs):
        gt_list = self.get_ground_truth_timestamp(timestamp, ground_truth)
        all_vehicles = self._percept_all_vehicles(gt_list)

        environment_model = EnvironmentModel(vehicle_id=self._ego_v_id)
        self.fill_environment_model(
            self._ego_v_id,
            environment_model,
            ground_truth,
            all_vehicles,
            self.per_pos_cov,
            self.per_vel_cov,
            self.loc_pos_cov,
            self.loc_vel_cov,
        )
        return environment_model

    @staticmethod
    def fill_environment_model(
        ego_id, environment_model, ground_truth, percepted_objects, per_pos_cov, per_vel_cov, loc_pos_cov, loc_vel_cov
    ):

        # add other vehicles
        for po in percepted_objects:
            po_state = po.timestamps.latest().state
            po_state.position.covariance = per_pos_cov
            po_state.velocity.covariance = per_vel_cov
            environment_model.add_object(
                po.id, po.appearance.color, po.appearance.length, po.appearance.width, po_state
            )

        # add ego vehicle
        ego_state = ground_truth[ego_id].timestamps.latest().state
        ego_state.position.covariance = loc_pos_cov
        ego_state.velocity.covariance = loc_vel_cov

        environment_model.add_object(
            ground_truth[ego_id].id,
            ground_truth[ego_id].appearance.color,
            ground_truth[ego_id].appearance.length,
            ground_truth[ego_id].appearance.width,
            ego_state,
        )

    def _percept_all_vehicles(self, ground_truth):
        """Percept all vehicles except the ego-vehicle"""
        percepted_objects = []
        for gt_v in ground_truth:
            if gt_v.id != self._ego_v_id:
                percepted_objects.append(gt_v)
        return percepted_objects

    @staticmethod
    def get_ground_truth_timestamp(timestamp, ground_truth):
        """Get ground-truth objects present in current timestamp by adding pointers"""
        gt_list = []
        for gt_v in list(ground_truth.values()):
            if gt_v.timestamps.latest().timestamp == timestamp:
                gt_list.append(gt_v)
        return gt_list
