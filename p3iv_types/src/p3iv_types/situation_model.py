import warnings
from p3iv_types.situation_object import SituationObject


class SituationModel(object):
    def __init__(self, scene_model=None):
        self._situation_objects = {}

        if scene_model:
            for s in scene_model.objects():
                self._situation_objects[s.v_id] = SituationObject(s)

    @property
    def situation_objects(self):
        return self._situation_objects

    def get_object(self, vehicle_id):
        return self._situation_objects[vehicle_id]

    def objects(self):
        return self._situation_objects.values()

    def add(self, situation_object):
        assert isinstance(situation_object, SituationObject)
        self._situation_objects[situation_object.v_id] = situation_object
