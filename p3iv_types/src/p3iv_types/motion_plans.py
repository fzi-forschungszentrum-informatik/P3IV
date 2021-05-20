import numpy as np
from p3iv_types.motion_state import MotionStateArray


class MotionPlan(object):
    def __init__(self):
        self.motion = MotionStateArray()
        self.details = dict()
        self.cost = None


class MotionPlans(list):
    def __init__(self):
        list.__init__(self)

    def append(self, arg):
        self.typecheck(arg)
        super(MotionPlans, self).append(arg)

    @staticmethod
    def typecheck(arg):
        assert isinstance(arg, MotionPlan)


# todo: use dataclass when using Python3.6
# from dataclasses import dataclass
# @dataclass
# class MotionPlan:
# ...
