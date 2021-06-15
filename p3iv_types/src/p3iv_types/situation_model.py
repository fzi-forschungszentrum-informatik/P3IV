import warnings
from p3iv_types.situation_object import SituationObject


class SituationModel(object):
    def __init__(self, scene_model=None):
        self._situation_objects = {}

        if scene_model:
            for s in scene_model.objects():
                self._situation_objects[s.id] = SituationObject(s)

    @property
    def situation_objects(self):
        return self._situation_objects

    def get_object(self, object_id):
        return self._situation_objects[object_id]

    def objects(self):
        return list(self._situation_objects.values())

    def add(self, situation_object):
        assert isinstance(situation_object, SituationObject)
        self._situation_objects[situation_object.id] = situation_object
