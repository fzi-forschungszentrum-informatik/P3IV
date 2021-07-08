# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
from p3iv_utils_probability.distributions import UnivariateNormalDistribution, BivariateNormalDistribution
from p3iv_utils_probability.distributions import (
    UnivariateNormalDistributionSequence,
    BivariateNormalDistributionSequence,
)
from p3iv_utils.finite_differences import finite_differences
from p3iv_utils.helper_functions import get_yaw_angle


class MotionState(object):
    """
    Motion state information of an object.

    Attributes
    ----------
    position: BivariateNormalDistribution
        Current Cartesian position.
    yaw: UnivariateNormalDistribution
        Current yaw angle.
    velocity: BivariateNormalDistribution
        Current velocity.
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


class MotionStateArray(object):
    """
    The MotionSequMotionStateArrayence object contains the motion sequence of a vehicle.

    Attributes:
    ----------
    position: BivariateNormalDistributionSequence
        Position array
    yaw: UnivariateNormalDistributionSequence
        Yaw angle array
    velocity: BivariateNormalDistributionSequence
        Velocity array
    """

    __slots__ = ["position", "yaw", "velocity", "dt"]

    def __init__(self, dt=0.1, position=None):
        """
        Args:
        -----
        dt: float64
            The time step (default: 0.1)
        position:
            (numpy array or BivariateNormalDistributionSequence): The position of the vehicle (default: None)
        """
        self.dt = dt

        if position:
            self.__call__(position, dt)
        else:
            self.position = BivariateNormalDistributionSequence()
            self.yaw = UnivariateNormalDistributionSequence()
            self.velocity = BivariateNormalDistributionSequence()

    def __call__(self, position, dt, difference_type="backward"):
        """
        Calculate the velocity, acceleration and jerk sequences by a given position sequence.

        Args:
        -----
        position: ndarray or BivariateNormalDistributionSequence
            The position of the vehicle
        dt: float
            Sampling interval
        difference_type: str
            Type of finite differences. "forward" or "backward" (default: "backward")
        """

        self.dt = dt

        self.resize(len(position))
        if isinstance(position, BivariateNormalDistributionSequence):
            v, a, j = finite_differences(position.mean(), dt, difference_type=difference_type)
            self.position = position

        elif isinstance(position, np.ndarray):
            v, a, j = finite_differences(position, dt, difference_type=difference_type)
            self.position.mean = position
        else:
            raise Exception

        # todo@Sahin: covariance

        if v.size == 0:
            v = np.zeros([len(position), 2])

        self.velocity.mean = v
        self.yaw.mean = get_yaw_angle(self.position.mean)

    def __getitem__(self, item):
        m = MotionStateArray(dt=self.dt)
        m.resize(len(self.position[item]))
        m.position = self.position[item]
        m.yaw = self.yaw[item]
        m.velocity = self.velocity[item]
        return m

    def __len__(self):
        return len(self.position)

    def __repr__(self):
        pos_repr = "Position : \n" + self.position.__repr__() + "\n"
        yaw_repr = "Yaw : \n" + self.yaw.__repr__() + "\n"
        vel_repr = "Velocity : \n" + self.velocity.__repr__() + "\n"
        final = "-" * 79 + "\n"
        return pos_repr + yaw_repr + vel_repr + final

    """
    todo
    def __add__(self, other):
        assert (isinstance(other, MotionSequence))
        self.position = self.position + other.position
        self.velocity = self.velocity + other.velocity
        self.acceleration = self.acceleration + other.acceleration
        self.jerk = self.jerk + other.jerk

    def __sub__(self, other):
        assert (isinstance(other, MotionSequence))
        self.position = self.position - other.position
        self.velocity = self.velocity - other.velocity
        self.acceleration = self.acceleration - other.acceleration
        self.jerk = self.jerk - other.jerk
    """

    def resize(self, n):
        """
        Change the sizes of the pre-allocated empty attributes according to the column number n.
        """
        self.position.resize(n)
        self.yaw.resize(n)
        self.velocity.resize(n)

    def append(self, other):
        """
        Append other MotionStateArray object
        """
        assert isinstance(other, MotionStateArray)
        self.position.append(other.position)
        self.yaw.append(other.yaw)
        self.velocity.append(other.velocity)

    @property
    def speed(self):
        return np.linalg.norm(self.velocity.mean, axis=1)
