# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import unittest
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from p3iv_visualization.cartesian.uncertainty_ellipse import UncertaintyEllipse


class PlotUncertaintyEllipseTest(unittest.TestCase):
    def test_plot_vehicle(self):
        fig, ax = plt.subplots(1, 1)
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)

        ellipse = UncertaintyEllipse("blue")
        ax.add_patch(ellipse.e)
        ellipse.update_transformation(3, 4, 45)
        ellipse.update_transformation(-3, 0, 22.5)
        ellipse.update_uncertainty(20, 8)
        plt.show()


if __name__ == "__main__":
    unittest.main()
