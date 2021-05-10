from __future__ import division
import matplotlib.image as mpimg
from matplotlib.transforms import Affine2D


class CarImage(object):
    def __init__(self, car_img_path, l_max=2.75):
        self.image = mpimg.imread(car_img_path)  # value is a :class:`numpy.array`
        self.l_max = l_max
        self.l_x = self.image.shape[0]
        self.l_y = self.image.shape[1]
        self.r = self.l_y / self.l_x

    def get_extend(self):
        # The location, in data-coordinates, of the lower-left and upper-right corners
        return [0, self.r * self.l_max, 0, self.l_max]

    def get_center(self):
        # return x and y
        return [self.r * self.l_max / 2, self.l_max / 2]

    def transform(self, x, y, yaw):
        image_x, image_y = self.get_center()
        rotate_around_center = Affine2D().rotate_deg_around(image_x, image_y, yaw)
        translate_center = Affine2D().translate(x - image_x, y - image_y)
        return rotate_around_center + translate_center


if __name__ == "__main__":
    import os
    import matplotlib.pyplot as plt

    # read the image
    path_file = os.path.dirname(os.path.realpath(__file__))
    path_img = os.path.join(path_file, "../res/car.png")

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
