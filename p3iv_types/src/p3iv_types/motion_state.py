from __future__ import division
import numpy as np
from util_probability.distributions import UnivariateNormalDistribution
from util_probability.distributions import BivariateNormalDistribution


class MotionState(object):
    """
    Motion state information of an object.

    Attributes
    ----------
    position: Bivariate normal distribution
        Current Cartesian position.
    yaw: Univariate normal distribution
        Current yaw angle.
    velocity: Bivariate normal distribution
        Current speed.
    """

    __slots__ = ["position", "yaw", "velocity"]

    def __init__(self):
        self.position = BivariateNormalDistribution()
        self.yaw = UnivariateNormalDistribution()
        self.velocity = BivariateNormalDistribution()

    @property
    def speed(self):
        return np.linalg.norm(self.velocity.mean)

    @property
    def pose(self):
        return np.hstack([self.position.mean, self.yaw.mean])
