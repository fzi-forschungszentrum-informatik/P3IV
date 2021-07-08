# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

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
