# This file is part of the Interpolated Polyline (https://github.com/...),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)


from p3iv_utils_polyline.interpolated_polyline import InterpolatedPolyline
from p3iv_utils_polyline.visualization.plot_distance_contours import main as plot_distance_contours
import unittest
import numpy as np


class InterpolatedPolylineInterpTest(unittest.TestCase):
    def test(self):

        o = np.array([[141, 31], [152, 31], [163, 31], [163, 27], [152, 27], [141, 27]])

        ox = o[:, 0]
        oy = o[:, 1]
        obs_ip = InterpolatedPolyline(ox, oy)
        plot_distance_contours(o, obs_ip, offset=10.0, show=False)

        self.assertAlmostEqual(obs_ip.signed_distance(153, 31), 0)
        self.assertLessEqual(obs_ip.signed_distance(153, 30), 0)
        self.assertLessEqual(obs_ip.signed_distance(153, 29), 0)
        self.assertLessEqual(obs_ip.signed_distance(153, 28), 0)
        self.assertAlmostEqual(obs_ip.signed_distance(153, 27), 0)


class InterpolatedPolylineLessInterpTest(unittest.TestCase):
    def test(self):
        o = np.array(
            [
                [141, 31],
                [142, 31],
                [152, 31],
                [158, 31],
                [163, 31],
                [163, 27],
                [158, 27],
                [152, 27],
                [142, 27],
                [141, 27],
            ]
        )

        ox = o[:, 0]
        oy = o[:, 1]
        obs_ip = InterpolatedPolyline(ox, oy)
        plot_distance_contours(o, obs_ip, offset=10.0, show=False)

        self.assertAlmostEqual(obs_ip.signed_distance(153, 31), 0)
        self.assertLessEqual(obs_ip.signed_distance(153, 30), 0)
        self.assertLessEqual(obs_ip.signed_distance(153, 29), 0)
        self.assertLessEqual(obs_ip.signed_distance(153, 28), 0)
        self.assertAlmostEqual(obs_ip.signed_distance(153, 27), 0)


if __name__ == "__main__":
    unittest.main()
