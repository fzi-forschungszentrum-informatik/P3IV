import unittest
import numpy as np
from p3iv_types.motion_state import MotionState, MotionStateArray


class MotionStateTest(unittest.TestCase):
    def test_empty(self):
        MotionState()


class MotionStateArrayTest(unittest.TestCase):
    def test_empty(self):
        MotionStateArray()

    def test_mp(self):
        pos = np.array([[1, 0], [2, 2], [3, 3], [4, 4]])
        m = MotionStateArray()
        m(pos, dt=0.1)
        print(m)
        print((m.position))
        print((m[1]))
        print((m[:2]))
        m1 = m
        m2 = m
        m.append(m1)
        # print(m1 + m2)
        # print(m1 - m2)


if __name__ == "__main__":
    unittest.main()
