from __future__ import division
import unittest
import numpy as np
from p3iv_utils.coordinate_transformation import CoordinateTransform
from util_probability.distributions import BivariateNormalDistributionSequence
from p3iv_visualization.motion.plot_array2d import PlotArray2D
from p3iv_visualization.motion.plot_motion_components import PlotMotionComponents
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class PlotArray2dTest(unittest.TestCase):
    def test_array2d(self):
        fig, ax = plt.subplots(1, 1)
        p = PlotArray2D(ax, "Timesteps")

        timesteps_ = np.arange(12) * 0.5
        p.initialize(timesteps_)
        p.set_x_axis()
        p.set_y_axis(-2, 20, increment=3)

        motion_array2d = np.zeros(24).reshape(-1, 2)
        motion_array2d[:, 0] = 5 * np.ones(12) + np.arange(12)
        motion_array2d[:, 1] = 4 * np.ones(12)
        p.update_motion_array2d(motion_array2d, index4pin2free=5)

        plt.show()


class PlotMotionComponentsTest(unittest.TestCase):
    def setUp(self):
        self.position = np.array(
            [
                [4.92560704e01, 1.41206491e-15],
                [5.00560704e01, -1.81126815e-15],
                [5.08560704e01, 2.98372438e-16],
                [5.17232704e01, -1.14838694e-15],
                [5.27024704e01, 2.06952511e-15],
                [5.37936704e01, -1.87350135e-15],
                [5.49999075e01, -1.08940634e-15],
                [5.63190916e01, 2.49800181e-15],
                [5.77454961e01, -1.29236899e-15],
                [5.92709730e01, -2.76861867e-15],
                [6.08859243e01, -4.51881314e-16],
                [6.25800593e01, -4.71844785e-16],
                [6.43429694e01, -4.57966998e-16],
                [6.61645485e01, 8.67361738e-16],
            ]
        )

        self.velocity = np.array(
            [
                [0.00000000e00, 0.00000000e00],
                [4.00000000e00, -1.61166653e-14],
                [4.00000000e00, 1.05482029e-14],
                [4.33600000e00, -7.23379689e-15],
                [4.89600000e00, 1.60895602e-14],
                [5.45600000e00, -1.97151323e-14],
                [6.03118564e00, 3.92047506e-15],
                [6.59592080e00, 1.79370407e-14],
                [7.13202224e00, -1.89518540e-14],
                [7.62738442e00, -7.38124839e-15],
                [8.07475648e00, 1.15836868e-14],
                [8.47067513e00, -9.98173551e-17],
                [8.81455030e00, 6.93889390e-17],
                [9.10789555e00, 6.62664368e-15],
            ]
        )

        self.acceleration = np.array(
            [
                [0.00000000e00, 0.00000000e00],
                [0.00000000e00, 0.00000000e00],
                [-1.77635684e-13, 1.33324341e-13],
                [1.68000000e00, -8.89099992e-14],
                [2.80000000e00, 1.16616786e-13],
                [2.80000000e00, -1.79023463e-13],
                [2.87592818e00, 1.18178037e-13],
                [2.82367581e00, 7.00828284e-14],
                [2.68050723e00, -1.84444474e-13],
                [2.47681090e00, 5.78530279e-14],
                [2.23686028e00, 9.48246758e-14],
                [1.97959324e00, -5.84175206e-14],
                [1.71937588e00, 8.46031470e-16],
                [1.46672621e00, 3.27862737e-14],
            ]
        )

        self.jerk = np.array(
            [
                [0.00000000e00, 0.00000000e00],
                [0.00000000e00, 0.00000000e00],
                [0.00000000e00, 0.00000000e00],
                [8.40000000e00, -1.11117170e-12],
                [5.60000000e00, 1.02763392e-12],
                [-9.76996262e-12, -1.47820124e-12],
                [3.79640891e-01, 1.48600750e-12],
                [-2.61261842e-01, -2.40476042e-13],
                [-7.15842895e-01, -1.27263651e-12],
                [-1.01848163e00, 1.21148751e-12],
                [-1.19975314e00, 1.84858239e-13],
                [-1.28633516e00, -7.66210982e-13],
                [-1.30108684e00, 2.96317760e-13],
                [-1.26324832e00, 1.59701211e-13],
            ]
        )

        self.timesteps = np.arange(len(self.position)) * 0.5

    def test_plot_motion_components(self):

        fig = plt.figure(1)

        gs = gridspec.GridSpec(3, 1)
        gs.update(hspace=0.00)
        ax0 = plt.subplot(gs[0, 0])
        ax1 = plt.subplot(gs[1, 0])
        ax2 = plt.subplot(gs[2, 0])

        p = PlotMotionComponents(ax0, ax1, ax2)
        p.initialize(self.timesteps)
        p.set_labels()
        p.update_profile(self.velocity, self.acceleration, self.jerk, index4pin2free=6)
        plt.show()


if __name__ == "__main__":
    unittest.main()
