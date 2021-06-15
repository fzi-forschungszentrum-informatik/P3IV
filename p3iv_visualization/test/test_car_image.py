
import unittest
import os
import matplotlib.pyplot as plt
from p3iv_visualization.cartesian.car_image import CarImage


class PlotCarImageTest(unittest.TestCase):
    def test_car_image(self):
        path_file = os.path.dirname(os.path.realpath(__file__))
        path_img = os.path.join(path_file, "../src/p3iv_visualization/res/car.png")

        # instantiate the class
        car_img = CarImage(path_img)
        ext = car_img.get_extend()

        fig, ax = plt.subplots(1, 1)
        im = ax.imshow(car_img.image, aspect="equal", interpolation="none", origin="lower", extent=ext)

        # image rotation & translation transformations
        center_x, center_y, rotation_deg = 5, 6, 45
        transform = car_img.transform(center_x, center_y, rotation_deg)
        trans_data = transform + im.get_transform()  # to be able to apply a transformation, initial tr is req.
        im.set_transform(trans_data)

        transform = car_img.transform(3, 3, 15)
        trans_data = transform + im.get_transform()
        im.set_transform(trans_data)

        # plot borders and the center point
        x1, x2, y1, y2 = im.get_extent()
        ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], "y--", transform=trans_data, color="red")
        ax.plot([(x1 + x2) / 2], [(y1 + y2) / 2], "*", ms=3, transform=trans_data, color="red")

        plt.show()


if __name__ == "__main__":
    unittest.main()
