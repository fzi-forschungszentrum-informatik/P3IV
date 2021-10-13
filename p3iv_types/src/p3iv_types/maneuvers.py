# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import uuid
import numpy as np
from enum import Enum
from copy import deepcopy
from p3iv_types.motion import MotionStateArray


class ManeuverIntentions(Enum):
    """Intention of object to host"""

    follow = 0
    lead = 1
    unclear = 2


class ManeuverProbability(object):
    def __init__(self):
        self.route = 1.0
        self.intention = 1.0
        self.maneuver = 0.0

    def __add__(self, other):
        assert isinstance(other, ManeuverProbability)
        self.route += other.route
        self.intention += other.intention
        self.maneuver += other.maneuver
        return self


class ManeuverBounds(object):
    def __init__(self, dt, N):
        self.dt = dt
        self.N = N

        self.time_horizon = np.arange(self.N) * self.dt

        self._upper_pos_bound = None
        self._lower_pos_bound = None
        self._upper_spd_bound = None
        self._lower_spd_bound = None

        self.applied_intention = None

    def __eq__(self, other):
        return (
            self.dt == other.dt
            and self.N == other.N
            and (np.abs(self._upper_pos_bound - other.upper_pos_bound) < 1e-6).all()
            and (np.abs(self._lower_pos_bound - other.lower_pos_bound) < 1e-6).all()
            and (np.abs(self._upper_spd_bound - other.upper_spd_bound) < 1e-6).all()
            and (np.abs(self._lower_spd_bound - other.lower_spd_bound) < 1e-6).all()
        )

    @property
    def upper_pos_bound(self):
        return self._upper_pos_bound

    @upper_pos_bound.setter
    def upper_pos_bound(self, v):
        self._upper_bound_setter("_upper_pos_bound", v)

    @property
    def lower_pos_bound(self):
        return self._lower_pos_bound

    @lower_pos_bound.setter
    def lower_pos_bound(self, v):
        self._lower_bound_setter("_lower_pos_bound", v)

    @property
    def upper_spd_bound(self):
        return self._upper_spd_bound

    @upper_spd_bound.setter
    def upper_spd_bound(self, v):
        self._upper_bound_setter("_upper_spd_bound", v)

    @property
    def lower_spd_bound(self):
        return self._lower_spd_bound

    @lower_spd_bound.setter
    def lower_spd_bound(self, v):
        self._lower_bound_setter("_lower_spd_bound", v)

    def _lower_bound_setter(self, attribute, value):
        if getattr(self, attribute) is not None:
            value = np.max([getattr(self, attribute), value], axis=0)
        setattr(self, attribute, value)

    def _upper_bound_setter(self, attribute, value):
        if getattr(self, attribute) is not None:
            value = np.min([getattr(self, attribute), value], axis=0)
        setattr(self, attribute, value)


class ManeuverHypothesis(object):
    """
    Contains (applies) assumptions on the dynamics of other vehicles; i.e. intentions
    Current position is the reference coordinate frame (0.0, 0.0)
    """

    __slots__ = [
        "id",
        "path",
        "dt",
        "N",
        "horizon",
        "motion",
        "progress",
        "overlap",
        "probability",
        "speed_limit",
        "maneuver_bounds",
    ]

    def __init__(self, current_state, progress, laneletpath, speed_limits, dt, N, horizon):
        self.id = uuid.uuid4()
        self.path = laneletpath
        self.dt = dt
        self.N = N
        self.horizon = horizon
        self.motion = MotionStateArray()
        self.motion.resize(self.N + 1)
        self.motion.position.mean[0] = current_state.position.mean
        self.motion.velocity.mean[0] = current_state.velocity.mean
        self.progress = np.zeros(self.N + 1)
        self.progress[0] = progress
        self.overlap = [False] * (self.N + 1)  # if position has any overlap with own ego/host-route
        self.probability = ManeuverProbability()
        self.speed_limit = speed_limits[0]

        # variables to create an output motion
        self.maneuver_bounds = ManeuverBounds(self.dt, self.N)
        self.maneuver_bounds.upper_pos_bound = np.arange(1, self.N + 1) * self.speed_limit * self.dt
        self.maneuver_bounds.upper_spd_bound = np.ones(self.N) * self.speed_limit  # todo: consider current speed
        self.maneuver_bounds.lower_pos_bound = np.zeros(self.N)
        self.maneuver_bounds.lower_spd_bound = np.zeros(self.N)

    def __eq__(self, other):
        return self.maneuver_bounds == other.maneuver_bounds

    def clone(self):
        clone_ = deepcopy(self)
        clone_.id = uuid.uuid4()
        return clone_


class ManeuverHypotheses(object):
    def __init__(self):
        self._hypotheses = []

    def __len__(self):
        return len(self._hypotheses)

    def add(self, maneuver_hypotheses):
        for mh in maneuver_hypotheses:
            self._hypotheses.append(mh)

    @property
    def hypotheses(self):
        return self._hypotheses

    @hypotheses.setter
    def hypotheses(self, h):
        self._hypotheses = h
