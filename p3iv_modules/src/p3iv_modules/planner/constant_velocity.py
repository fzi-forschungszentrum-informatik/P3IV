# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
from p3iv_modules.interfaces.planning import PlannerInterface
from p3iv_types.motion import MotionPlan, MotionPlans
from p3iv_utils.coordinate_transformation import CoordinateTransform


class Planner(PlannerInterface):
    def __init__(self, ego_id, ego_width, ego_length, configurations, *args, **kwargs):
        super(Planner, self).__init__(ego_id, ego_width, ego_length, configurations, *args, **kwargs)
        self._id = ego_id
        self._width = ego_width
        self._length = ego_length
        self.dt = configurations["temporal"]["dt"] / 1000.0
        self.n = configurations["temporal"]["N"]
        self.timestamp = 0

        # store intermediate stuff for convenience
        self._coordinate_transform = None
        self._state = None
        self._progress = None

    def __call__(self, timestamp, state, scene_model, situation_model, decision_base, *args, **kwargs):
        PlannerInterface.type_check(timestamp, state, scene_model, situation_model, decision_base, *args, **kwargs)
        self.setCurrentTimestamp(timestamp)
        self.setDrivingCorridor(decision_base.corridor)

        foo = 0.0
        self.setMotionState(state, foo)
        mp = self.solve()

        mps = MotionPlans()
        mps.append(mp)
        return mps

    def setCurrentTimestamp(self, timestamp):
        assert isinstance(timestamp, int)
        self.timestamp = timestamp

    def setDrivingCorridor(self, corridor):
        self._corridor_centerline = corridor.center
        self._coordinate_transform = CoordinateTransform(self._corridor_centerline)

    def setMotionState(self, state, progress):
        self._state = state
        self._progress = progress

    def solve(self, *args, **kwargs):
        current_pos = self._progress
        profile = np.array([])
        for i in range(self.n):
            new_pos = current_pos + self._state.speed * self.dt
            profile = np.append(profile, new_pos)
            current_pos = new_pos
        frenet_l = np.append(self._progress, profile)

        xy = self._coordinate_transform.expand(self._state.position.mean, frenet_l, ignore_lateral_offset=True)
        mp = MotionPlan()
        mp.motion(xy, dt=self.dt)

        PlannerInterface.overwrite_with_current_state(mp, self._state)

        assert len(mp.motion) == self.n + 1  # 1-> current state
        return mp
