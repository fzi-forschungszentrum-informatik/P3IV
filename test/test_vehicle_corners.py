import unittest
import numpy as np
import matplotlib.pyplot as plt
from p3iv.types.vehicle import Vehicle


class TestVehicleCorners(unittest.TestCase):
    def setUp(self):
        self.vehicle = Vehicle(0)
        self.vehicle.appearance.length = 5.2
        self.vehicle.appearance.width = 1.8

    def test_corners(self):
        xy = np.array([3, 3])
        for theta in np.linspace(-420, 420, 100):
            self.vehicle.appearance.get_corners(xy, theta)

    def test_corners_w_plot(self):
        xy = np.array([3, 3])

        fig = plt.figure()
        plt.xlim(xy[0] - 10, xy[0] + 10)
        plt.ylim(xy[1] - 10, xy[1] + 10)
        plt.gca().set_aspect('equal', adjustable='box')

        for theta in np.linspace(-420, 420, 50):
            c = self.vehicle.appearance.get_corners(xy, theta)
            for c_ in c:
                plt.scatter(c_[0], c_[1], color='red', marker='o')
        plt.show()


if __name__ == "__main__":
    unittest.main()
