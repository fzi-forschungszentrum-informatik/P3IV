import unittest
import numpy as np
from p3iv_types.environment_model import EnvironmentModel
from p3iv_types.motion_state import MotionState


class TestEnvironmentModel(unittest.TestCase):
    def test_environment_model(self):

        m0 = MotionState()
        m0.position.mean = np.asarray([998.0, 1016.0])  # @ll 30048

        m1 = MotionState()
        m1.position.mean = np.asarray([1011.0, 982.0])  # @ll 30015

        m2 = MotionState()
        m2.position.mean = np.asarray([1013.0, 986.0])  # @ll 30041

        m3 = MotionState()
        m3.position.mean = np.asarray([1018.0, 986.0])  # @ll 30041

        m4 = MotionState()
        m4.position.mean = np.asarray([1023.0, 967.0])  # @ll 30055

        m5 = MotionState()
        m5.position.mean = np.asarray([998.0, 1027.0])  # @ll 30048

        e = EnvironmentModel()
        e.add_object(0, "blue", 2.8, 1.8, m0)
        e.add_object(1, "yellow", 2.8, 1.8, m1)
        e.add_object(2, "orange", 2.8, 1.8, m2)
        e.add_object(3, "salmon", 2.8, 1.8, m3)
        e.add_object(4, "black", 2.8, 1.8, m4)
        e.add_object(5, "red", 2.8, 1.8, m5)


if __name__ == "__main__":
    unittest.main()
