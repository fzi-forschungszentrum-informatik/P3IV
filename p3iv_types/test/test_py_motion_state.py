# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import unittest
import numpy as np
from p3iv_types.py_motion import PyMotionState, PyMotionStateArray


class PyMotionStateTest(unittest.TestCase):
    def test_empty(self):
        m = PyMotionState()
        mean = np.asarray([4.0, 0.0])
        cov = np.asarray([16.0, 0.0, 0.0, 16.0])
        m.setPosition(mean, cov)
        m.setYaw(mean[:1], cov[:1])
        m.setVelocity(mean, cov)


class PyMotionStateArrayTest(unittest.TestCase):
    def test_empty(self):
        PyMotionStateArray()

    def test_mp(self):
        m = PyMotionStateArray()
        mean = np.asarray([4.0, 0.0, 4.0, 0.0])
        cov = np.asarray([16.0, 0.0, 0.0, 16.0, 16.0, 0.0, 0.0, 16.0])
        m.setPosition(mean, cov)


if __name__ == "__main__":
    unittest.main()
