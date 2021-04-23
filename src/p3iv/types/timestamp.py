from collections import OrderedDict


class Timestamps(object):
    def __init__(self):
        self._timestamps = OrderedDict()

    def __len__(self):
        return len(self._timestamps)

    def __call__(self, *args, **kwargs):
        return self._timestamps.values()

    def add(self, timestamp, timestamp_data):
        assert (isinstance(timestamp, int))
        assert (isinstance(timestamp_data, TimestampData))
        self._timestamps[str(timestamp)] = timestamp_data

    def create_and_add(self, timestamp):
        # todo@Sahin: good practice??
        timestamp_data = TimestampData(timestamp)
        self.add(timestamp, timestamp_data)

    def get(self, timestamp=None):
        if timestamp is None:
            return self._timestamps.values()[-1]
        else:
            return self._timestamps[str(timestamp)]

    def latest(self):
        return next(reversed(self._timestamps.values()))

    def previous(self):
        return self._timestamps.values()[-2]


class TimestampData(object):
    def __init__(self, timestamp):
        assert (isinstance(timestamp, int))
        self.timestamp = timestamp
        self.motion = None
        self.localization = None  # LocalizationModel class
        self.environment = None   # EnvironmentModel class
        self.scene = None   # SceneModel class
        self.situation = None   # SituationModel class
        self.decision_base = None   # DecisionBase class
        self.motion_plans = None   # MotionPlans class in local Frenet-Frame
        self.plan_optimal = None  # optimal MotionPlan in global Frenet-frame
