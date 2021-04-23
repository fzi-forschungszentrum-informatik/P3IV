from __future__ import division
from p3iv.types.vehicle import VehicleAppearance
from util_motion.motion_sequence import MotionSequence


class ExistenceProbability(object):
    def __init__(self):
        super(ExistenceProbability, self).__init__()
        self._existence_probability = 1.0

    @property
    def existence_probability(self):
        return self._existence_probability

    @existence_probability.setter
    def existence_probability(self, probability):
        assert (0.0 <= probability <= 1.0)
        self._existence_probability = probability


class TrackedObject(VehicleAppearance, ExistenceProbability):
    """
    Contains information on a detected vehicle.

    Attributes
    ---------
    _v_id : int
        Vehicle id
    _color : str
        Vehicle color
    motion : MotionSequence
        Tracked motion until current timestamp
    current_lanelets : list
        Contains list of current Lanelets the object might be on
    """
    def __init__(self):
        super(TrackedObject, self).__init__()
        self._v_id = 0
        self._color = "black"  # override appearance
        self.motion = MotionSequence()
        self.current_lanelets = None

    @property
    def v_id(self):
        return self._v_id

    @v_id.setter
    def v_id(self, vehicle_id):
        assert isinstance(vehicle_id, int)
        self._v_id = vehicle_id

    @property
    def yaw(self):
        return self.motion.yaw_angle[-1]

    @property
    def position(self):
        return self.motion.cartesian.position.mean[-1]

    @property
    def velocity(self):
        return self.motion.cartesian.velocity.mean[-1]

    @property
    def acceleration(self):
        return self.motion.cartesian.acceleration.mean[-1]
