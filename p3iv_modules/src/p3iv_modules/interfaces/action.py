# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import abc
import p3iv_types


class ActInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, motion_plans, *args, **kwargs):
        """
        Given a MotionPlans instance containing at least one MotionPlan, pick the optimal one.

        Parameters
        ----------
        motion_plans: MotionPlans
            Current timestamp value.

        Returns
        -------
        motion_plan: MotionPlan
            The optimal motion plan
        """
        self.type_check(motion_plans)
        pass

    @staticmethod
    def type_check(motion_plans):
        assert isinstance(motion_plans, p3iv_types.MotionPlans)
