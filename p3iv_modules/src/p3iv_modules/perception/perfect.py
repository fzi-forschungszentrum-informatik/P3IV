from __future__ import absolute_import
from p3iv_modules.interfaces.perception import PerceptInterface
from p3iv_types.environment_model import EnvironmentModel


class Percept(PerceptInterface):
    def __init__(self, ego_v_id, pos_sigma_x, pos_sigma_y, pos_cross_corr, *args, **kwargs):
        self._ego_v_id = ego_v_id

    def __call__(self, timestamp, ground_truth, *args, **kwargs):
        gt_list = self.get_ground_truth_timestamp(timestamp, ground_truth)
        all_vehicles = self._percept_all_vehicles(gt_list)

        environment_model = EnvironmentModel(vehicle_id=self._ego_v_id)
        self.fill_environment_model(self._ego_v_id, environment_model, ground_truth, all_vehicles)
        return environment_model

    @staticmethod
    def fill_environment_model(ego_id, environment_model, ground_truth, percepted_objects):
        for po in percepted_objects:
            environment_model.add_object(
                po.id, po.appearance.color, po.appearance.length, po.appearance.width, po.timestamps.latest().state
            )

        # add the vehicle itself into EnvironmentModel
        environment_model.add_object(
            ground_truth[ego_id].id,
            ground_truth[ego_id].appearance.color,
            ground_truth[ego_id].appearance.length,
            ground_truth[ego_id].appearance.width,
            ground_truth[ego_id].timestamps.latest().state,
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
        for gt_v in ground_truth.values():
            if gt_v.timestamps.latest().timestamp == timestamp:
                gt_list.append(gt_v)
        return gt_list
