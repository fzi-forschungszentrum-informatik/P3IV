from __future__ import division
from prediction.maneuver_identifier.types.maneuver_hypotheses import ManeuverHypotheses
from p3iv_types.scene_object import SceneObject


class SituationObject(object):
    def __init__(self, *args, **kwargs):
        self.v_id = None
        self.maneuvers = ManeuverHypotheses()  # current maneuver hypothesis of the current timestep
        self.crossing_voi_route = None

        if type(args[0]) is SceneObject:
            self.v_id = args[0].v_id
            self.crossing_voi_route = args[0].crossing_voi_route
            # raw_input("todo - crossing voi route of situation object --> do that for path options")
