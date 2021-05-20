from __future__ import division, absolute_import
import numpy as np
from util_probability.distributions import UnivariateNormalDistribution, BivariateNormalDistribution
from util_probability.distributions import UnivariateNormalDistributionSequence, BivariateNormalDistributionSequence
from p3iv_utils.finite_differences import finite_differences


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
            self.position = position.mean()

        elif isinstance(position, np.ndarray):
            v, a, j = finite_differences(position, dt, difference_type=difference_type)
            self.position.mean = position
        else:
            raise Exception

        # todo@Sahin: covariance

        if v.size == 0:
            v = np.zeros([len(position), 2])
        if a.size == 0:
            a = np.zeros([len(position), 2])
        if j.size == 0:
            j = np.zeros([len(position), 2])

        self.velocity.mean = v
        # todo@Sahin
        self.yaw.mean = a

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
        repr = "position : \n" + self.position.__repr__()
        return repr

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
