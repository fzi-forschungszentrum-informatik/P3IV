import unittest
import numpy as np
from p3iv.types.environment_model import EnvironmentModel
from util_motion.motion import Motion


class TestEnvironmentModel(unittest.TestCase):
    def test_environment_model(self):

        m0 = Motion()
        m0.resize(1)
        m0.cartesian.position.mean[0] = np.asarray([998.0, 1016.0])  # @ll 30048

        m1 = Motion()
        m1.resize(1)
        m1.cartesian.position.mean[0] = np.asarray([1011.0, 982.0])  # @ll 30015

        m2 = Motion()
        m2.resize(1)
        m2.cartesian.position.mean[0] = np.asarray([1013.0, 986.0])  # @ll 30041

        m3 = Motion()
        m3.resize(1)
        m3.cartesian.position.mean[0] = np.asarray([1018.0, 986.0])  # @ll 30041

        m4 = Motion()
        m4.resize(1)
        m4.cartesian.position.mean[0] = np.asarray([1023.0, 967.0])  # @ll 30055

        m5 = Motion()
        m5.resize(1)
        m5.cartesian.position.mean[0] = np.asarray([998.0, 1027.0])  # @ll 30048

        e = EnvironmentModel()
        e.add_object(0, "blue", 2.8, 1.8, m0)
        e.add_object(1, "yellow", 2.8, 1.8, m1)
        e.add_object(2, "orange", 2.8, 1.8, m2)
        e.add_object(3, "salmon", 2.8, 1.8, m3)
        e.add_object(4, "black", 2.8, 1.8, m4)
        e.add_object(5, "red", 2.8, 1.8, m5)


if __name__ == "__main__":
    unittest.main()
