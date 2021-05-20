from __future__ import division
import unittest
import numpy as np
from p3iv_utils.finite_differences import finite_differences


class CheckFiniteDifferences(unittest.TestCase):
    def test(self):
        pos_cartesian = np.array([[1, 0], [2, 2], [3, 3], [5, 3]])
        v, a, j = finite_differences(pos_cartesian, dt=0.1)

        self.assertEqual(v[-1, 0], (pos_cartesian[-1, 0] - pos_cartesian[-2, 0]) / 0.1)
        self.assertEqual(v[-1, 0], 20)
        self.assertEqual(v[-1, 1], 0)
        self.assertEqual(a[-1, 0], (v[-1, 0] - v[-2, 0]) / 0.1)
        self.assertEqual(j[-1, 0], (a[-1, 0] - a[-2, 0]) / 0.1)
