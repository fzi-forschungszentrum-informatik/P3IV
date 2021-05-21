from __future__ import division, absolute_import
import unittest
import numpy as np
import matplotlib.pyplot as plt
from p3iv_utils.coordinate_transformation import CoordinateTransform


class Visualizer(object):
    def __init__(self, c_cartesian, c_frenet):
        self.c_cartesian = c_cartesian

        self.fig = plt.figure(figsize=(7, 8))
        self.ax_cartesian = self.fig.add_subplot(2, 1, 1)
        self.ax_frenet = self.fig.add_subplot(2, 1, 2)

        self.ax_cartesian.plot(c_cartesian[:, 0], c_cartesian[:, 1])
        self.ax_frenet.plot(c_frenet[:, 0], c_frenet[:, 1])

    def __call__(self, pos_cartesian, pos_frenet, plot_norm_flag=False, show=False):
        self.ax_cartesian.plot(pos_cartesian[:, 0], pos_cartesian[:, 1], "ro")
        self.ax_cartesian.set_title("Centerline and positions in Cartesian frame")
        self.ax_cartesian.set_xlabel("x (m)")
        self.ax_cartesian.set_ylabel("y (m)")

        self.ax_frenet.plot(pos_frenet[:, 0], pos_frenet[:, 1], "ro")
        self.ax_frenet.set_title("Centerline and positions in Frenet frame")
        self.ax_frenet.set_xlabel("s (m)")
        self.ax_frenet.set_ylabel("d (m)")

        vec = np.asarray(
            [[self.c_cartesian[1, :] - self.c_cartesian[0, :]], [self.c_cartesian[2, :] - self.c_cartesian[1, :]]]
        )
        vec = vec.reshape([-1, 2])
        if plot_norm_flag:
            self.plot_normal(self.c_cartesian[1, :], vec)

        plt.tight_layout()
        if show:
            plt.show()

    def plot_normal(self, origin, vec):
        n = np.zeros(vec.shape)
        # origin = origin[0], origin[1]
        for i in range(vec.shape[0]):
            n[i, 0] = -vec[i, 1]
            n[i, 1] = vec[i, 0]
            n[i, :] = n[i, :] / np.linalg.norm(vec[i, :])
        self.ax_cartesian.set_aspect("equal")
        # self.ax_frenet.set_aspect('equal')
        self.ax_cartesian.quiver(origin[0], origin[1], n[:, 0], n[:, 1], color="red", lw=0.25, width=0.0025, scale=8)

        for i in range(n.shape[0]):
            self.plot_points_on_normal(origin, n[i, :])

    def plot_points_on_normal(self, origin, normal):
        p = origin.reshape(-1, 2) + normal
        self.ax_cartesian.plot(p[0, 0], p[0, 1], "r*")
        print("abs(p - origin) = {}".format(np.linalg.norm(p - origin.reshape(-1, 2))))

        c = CoordinateTransform(self.c_cartesian)
        p_f = c.xy2ld(p)
        self.ax_frenet.plot(p_f[0, 0], p_f[0, 1], "r*")
        print("s, d = {:.4f}, {:.4f}".format(p_f[0, 0], p_f[0, 1]))
        self.ax_frenet.text(p_f[0, 0], p_f[0, 1] - 0.1, "({:.2f}. {:.2f})".format(p_f[0, 0], p_f[0, 1]))


class MotionLinearCenterlineTestVisualization(unittest.TestCase):
    def test(self):
        centerline = np.zeros([10, 2])
        centerline[:, 0] = np.arange(10)
        centerline[:, 1] = np.arange(10) * 0.5
        c = CoordinateTransform(centerline)

        self.pos_cartesian = np.array([[1, 0], [2, 2], [3, 3], [5, 3]])
        self.pos_frenet = c.xy2ld(self.pos_cartesian)

        centerline_frenet = c.xy2ld(centerline)
        v = Visualizer(centerline, centerline_frenet)
        v(self.pos_cartesian, self.pos_frenet)


class MotionNonlinearCenterlineTestVisualization(unittest.TestCase):
    def test(self):
        self.centerline = np.zeros([10, 2])
        self.centerline[:, 0] = np.arange(0, 10)
        self.centerline[:, 1] = 2 * self.centerline[:, 0] ** (1 / 2.4)
        c = CoordinateTransform(self.centerline)

        self.centerline_frenet = c.xy2ld(self.centerline)
        v = Visualizer(self.centerline, self.centerline_frenet)

        self.pos_cartesian = np.array([[0.75, 2.2], [2, 3], [4, 3.5], [7, 4.5]])
        self.pos_frenet = c.xy2ld(self.pos_cartesian)
        print(self.pos_frenet)

        v(self.pos_cartesian, self.pos_frenet, plot_norm_flag=True)


class Cartesian2ArcConversion(unittest.TestCase):
    def test_one(self):
        centerline = np.zeros([10, 2])
        centerline[:, 0] = np.arange(10)
        centerline[:, 1] = np.arange(10)

        c = CoordinateTransform(centerline)

        xy_0 = [4.0, 0.0]
        ld_0 = c.xy2ld(xy_0)
        self.assertAlmostEquals(np.sum(ld_0 - np.array([2.82842712, -2.82842712])), 0.0)

        xy_1 = [4.0, 8.0]
        ld_1 = c.xy2ld(xy_1)
        self.assertAlmostEquals(np.sum(ld_1 - np.array([8.48528137, 2.82842712])), 0.0)

    def test_two(self):

        centerline = np.zeros([10, 2])
        centerline[:, 0] = np.arange(10)
        centerline[:, 1] = np.arange(10) * 0.5
        c = CoordinateTransform(centerline)

        pos_cartesian = np.array([[1, 0], [2, 2], [3, 3], [5, 3]])
        pos_frenet = c.xy2ld(pos_cartesian)

        gt = np.array(
            [[0.89442719, -0.4472136], [2.68328157, 0.89442719], [4.02492236, 1.34164079], [5.81377674, 0.4472136]]
        )

        self.assertAlmostEquals(np.sum(pos_frenet - gt), 0.0)

    def test_three(self):

        centerline = np.zeros([10, 2])
        centerline[:, 0] = np.arange(0, 10)
        centerline[:, 1] = 2 * centerline[:, 0] ** (1 / 2.4)
        c = CoordinateTransform(centerline)

        pos_cartesian = np.array([[0.75, 2.2], [2, 3], [4, 3.5], [7, 4.5]])
        pos_frenet = c.xy2ld(pos_cartesian)

        gt = np.array(
            [[1.6546903, 1.63232962], [3.13049517, 1.78885438], [5.14295635, 1.34164079], [8.27345152, 0.89442719]]
        )

        self.assertLess(np.sum(pos_frenet - gt), 1e-6)


if __name__ == "__main__":
    unittest.main()
