# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import unittest
from p3iv_types.motion import MotionPlan, MotionPlans


class MotionPlansTest(unittest.TestCase):
    def test_empty(self):
        MotionPlans()

    def test_mp(self):
        mp1 = MotionPlan()
        mp2 = MotionPlan()
        mps = MotionPlans()
        mps.append(mp1)
        mps.append(mp2)


if __name__ == "__main__":
    unittest.main()
