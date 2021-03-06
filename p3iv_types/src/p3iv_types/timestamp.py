# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

from collections import OrderedDict


class Timestamps(object):
    """
    Container class to store timestamp data.

    Attributes
    ----------
    _timestamps: OrderedDict()
        Store TimestampData of individual timestamps
    """

    __slots__ = ["_timestamps"]

    def __init__(self):
        self._timestamps = OrderedDict()

    def __len__(self):
        return len(self._timestamps)

    def __call__(self, *args, **kwargs):
        return list(self._timestamps.values())

    def add(self, timestamp, timestamp_data):
        assert isinstance(timestamp, int)
        assert isinstance(timestamp_data, TimestampData)
        self._timestamps[str(timestamp)] = timestamp_data

    def create_and_add(self, timestamp):
        # todo@Sahin: good practice??
        timestamp_data = TimestampData(timestamp)
        self.add(timestamp, timestamp_data)

    def get(self, timestamp=None):
        if timestamp is None:
            return list(self._timestamps.values())[-1]
        else:
            return self._timestamps[str(timestamp)]

    def latest(self):
        return next(reversed(list(self._timestamps.values())))

    def previous(self):
        return list(self._timestamps.values())[-2]


class TimestampData(object):
    """
    Information stored for a certaint timestamp.

    Attributes
    ----------
    timestamp: int
        Current timestamp represented as an integer.
    state: VehicleState
        Current position and velocity information of a vehicle state.
    environment: EnvironmentModel
        Current environment model obtained from perception. Containts tracked object list
    scene: SceneModel
        Current scene model. Contains map-matched tracked objects.
    situation: SituationModel
        Current situation model. Contains predictions and reachability information.
    decision_base: DecisionBase
        Current decision base that is used to set constraints for homotopic motion plans.
    motion_plans: MotionPlans
        Currnet motion plans.
    plan_optimal: MotionPlan
        Optimal motion plan to execute in current timestamp.
    """

    __slots__ = [
        "timestamp",
        "state",
        "environment",
        "scene",
        "situation",
        "decision_base",
        "motion_plans",
        "plan_optimal",
    ]

    def __init__(self, timestamp):
        assert isinstance(timestamp, int)
        self.timestamp = timestamp
