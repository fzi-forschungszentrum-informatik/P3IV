# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import warnings
import matplotlib.image as mpimg
from matplotlib.axes import Axes
from matplotlib.transforms import Affine2D


map_configurations = dict()
map_configurations["DR_DEU_Roundabout_OF"] = {}
map_configurations["DR_DEU_Roundabout_OF"]["rotation_angle_deg"] = -17.4  # -17.5
map_configurations["DR_DEU_Roundabout_OF"]["x_center_par"] = 1 / 3
map_configurations["DR_DEU_Roundabout_OF"]["y_center_par"] = 1 / 3
map_configurations["DR_DEU_Roundabout_OF"]["x_offset"] = -15.3
map_configurations["DR_DEU_Roundabout_OF"]["y_offset"] = -27
map_configurations["DR_DEU_Roundabout_OF"]["map_scale"] = 0.43


class MapImagery(object):
    def __init__(self, axes, img_path, x_min, x_max, y_min, y_max, map_config=map_configurations):
        assert isinstance(axes, Axes)
        map_name = img_path.split("/")[-1].split(".")[0]
        if map_name not in list(map_config.keys()):
            warnings.warn("Map is not in map_configurations! Will fail!")

        # set values from initialization
        self._map_config = map_config[map_name]
        self._ax = axes
        self._xmin = x_min
        self._xmax = x_max
        self._ymin = y_min
        self._ymax = y_max

        # instance variables for processing
        self.l_max = abs(self._xmax - self._xmin)
        self.map_scale = 1
        self.rotation_angle_deg = 0
        self.x_offset = 0
        self.y_offset = 0

        try:
            self.background_image = mpimg.imread(img_path)
            self._set_transformation_parameters_from_config()
        except IOError:
            print((map_name + " not found!"))

    def get_extend(self):
        l_x = self.background_image.shape[0]
        l_y = self.background_image.shape[1]
        r = l_y / l_x  # r > 1
        return [0, self.map_scale * r * self.l_max, self.map_scale * self.l_max, 0]

    def get_center(self):
        _, x_range, _, y_range = self.get_extend()
        return [x_range * self._map_config["x_center_par"], y_range * self._map_config["y_center_par"]]

    def transform(self):
        image_x, image_y = self.get_center()
        rotate_around_center = Affine2D().rotate_deg_around(image_x, image_y, self.rotation_angle_deg)
        x = (self._xmin + self._xmax) / 2
        y = (self._ymin + self._ymax) / 2
        translate_center = Affine2D().translate(x - image_x + self.x_offset, y - image_y + self.y_offset)
        return rotate_around_center + translate_center

    def display_image(self):
        ext = self.get_extend()
        im = self._ax.imshow(
            self.background_image, aspect="equal", interpolation="none", origin="lower", extent=ext, alpha=0.7
        )
        trans_data = self.transform() + im.get_transform()
        im.set_transform(trans_data)

    def _set_transformation_parameters_from_config(self):
        self.map_scale = self._map_config["map_scale"]
        self.rotation_angle_deg = self._map_config["rotation_angle_deg"]
        self.x_offset = self._map_config["x_offset"]
        self.y_offset = self._map_config["y_offset"]
