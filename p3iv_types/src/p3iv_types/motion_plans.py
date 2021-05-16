import numpy as np
from util_motion.motion import Motion

# from solution_details import SolutionDetails


class MotionPlan(object):
    def __init__(self):
        self.motion = Motion()
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
