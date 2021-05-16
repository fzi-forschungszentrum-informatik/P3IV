from __future__ import division
import numpy as np
from p3iv_modules.interfaces.planning import PlannerInterface
from p3iv_types.motion_plans import MotionPlans
from utils import get_MotionPlan_from_1D


class Planner(PlannerInterface):
    def __init__(self, configurations, *args, **kwargs):
        super(Planner, self).__init__(configurations, *args, **kwargs)
        self.dt = configurations["temporal"]["dt"] / 1000
        self.n = configurations["temporal"]["N"]
        self.timestamp = 0

        # store intermediate stuff for convenience
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

        mp = get_MotionPlan_from_1D(self._corridor_centerline, self._state.position.mean, frenet_l, self.dt)
        assert len(mp.motion) == self.n + 1  # 1-> current state
        return mp
