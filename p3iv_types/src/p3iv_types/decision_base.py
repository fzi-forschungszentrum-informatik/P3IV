# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np


class DrivingCorridorCartesian(object):
    def __init__(self):
        self.left = None
        self.center = None
        self.right = None

    def __call__(self, left, center, right):
        assert isinstance(left, np.ndarray) and isinstance(center, np.ndarray) and isinstance(right, np.ndarray)
        self.left = left
        self.center = center
        self.right = right


class DecisionBase(object):
    """DecisionBase class augments the information provided by the
    understanding, prediction modules and resolves conflicts if any.

    Attributes
    ----------
    corridor : DrivingCorridorCartesian
        Cartesian coordinates of the DrivingCorridor. DrivingCorridor in Cartesian coord's are stored here. Whereas,
        their Lanelet counterparts are stored in SceneUnderstanding.
    motion_plans : List
        List of alternative Motions for the future
    """

    def __init__(self):
        self.corridor = DrivingCorridorCartesian()
        self.motion_plans = []

    def __call__(self, *args, **kwargs):
        pass

    def set_driving_corridor(self, laneletsequence, *args):
        self.corridor(
            laneletsequence.bound_left(), laneletsequence.centerline(smooth=True), laneletsequence.bound_right()
        )
