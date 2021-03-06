# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np
from .car_image import CarImage
from matplotlib.patches import Rectangle, Polygon
from .uncertainty_ellipse import UncertaintyEllipse
from matplotlib.collections import PatchCollection


class PlotVehicle(object):
    def __init__(self, ax, vehicle_id, color, car_width=2.3, car_length=5.8, alpha=1.0):
        self.ax = ax
        self.color = color
        self.alpha = alpha

        self.axesimage = None
        self.uncertainty_ellipse_68 = None  # matplotlib.patches.Ellipse, 68%
        self.uncertainty_ellipse_95 = None  # matplotlib.patches.Ellipse, 95%
        self.uncertainty_ellipse_99 = None  # matplotlib.patches.Ellipse, 99.7%
        self.uncertainty_ellipses = []

        self.ax.lines_line2d_track = None
        self.ax.lines_line2d_plan = None
        self.ax.lines_line2d_stop_pos = None

        self.rectangle_patch = None
        self.id_text = self.ax.text(0.0, 0.0, "ID" + str(vehicle_id), horizontalalignment="center", zorder=2.8)
        self.id_text.set_clip_on(True)
        self.speed_text = self.ax.text(0.0, 0.0, "")
        self.speed_text.set_clip_on(True)
        self.rectangle_width = car_length  # the corner. that is rotated in the Rectangle-Patch is the Rear-Right corner
        self.rectangle_height = car_width
        self._d = ((self.rectangle_width / 2) ** 2 + (self.rectangle_height / 2) ** 2) ** 0.5
        self._alpha = np.arctan2(self.rectangle_height / 2, self.rectangle_width / 2)
        self.car_image = None
        self.visible_area_patch = None

        self.axesimage_transform_initial = None

    def create_track(self):
        """
        Define a line for visualizing vehicle track.
        Be careful while using this together with other PlotVehicle instances!
        Matplotlib uses a single reference as self.ax is in __init__()!
        """

        (self.ax.lines_line2d_track,) = self.ax.plot([], [], marker="o", color=self.color, ms=3, linewidth=2)
        (self.ax.lines_line2d_plan,) = self.ax.plot([], [], marker="o", color=self.color, ms=3, linewidth=1, alpha=0.5)

    def update_track(self, motion_past, motion_future):
        self.ax.lines_line2d_track.set_data(motion_past[:, 0], motion_past[:, 1])
        self.ax.lines_line2d_plan.set_data(motion_future[:, 0], motion_future[:, 1])

    def set_car_image(self, car_img_path):
        self.car_image = CarImage(car_img_path)
        ext = self.car_image.get_extend()
        self.axesimage = self.ax.imshow(
            self.car_image.image, aspect="equal", interpolation="none", origin="lower", extent=ext, zorder=10
        )
        self.axesimage_transform_initial = self.axesimage.get_transform()

    def update_car_image(self, x, y, heading):
        transform = self.car_image.transform(x, y, heading)
        # todo: not clear why the initial transformation has to be set.
        trans_data = transform + self.axesimage_transform_initial
        self.axesimage.set_transform(trans_data)

    def set_car_patch(self):
        """Visualize vehicle as a polygon"""
        self.rectangle_patch = Rectangle(
            (0, 0),
            width=self.rectangle_width,
            height=self.rectangle_height,
            facecolor=self.color,
            edgecolor=self.color,
            alpha=self.alpha,
        )
        self.ax.add_patch(self.rectangle_patch)

    def update_car_patch_rear_axle(self, x, y, heading):
        angle = np.rad2deg(heading)
        x_ = x + self.rectangle_width / 2 * np.cos(180 + heading)
        y_ = y + self.rectangle_height / 2 * np.sin(180 + heading)
        self.rectangle_patch.set_xy((x_, y_))  # this is the left-bottom point
        self.rectangle_patch.angle = angle

    def update_speed_info_text(self, x_center, y_center, speed):
        self.speed_text.set_position([x_center + 3, y_center + 1])
        txt = "v=" + "{:.2f}".format(speed)
        self.speed_text.set_text(txt)

    def update_car_patch_center(self, x_center, y_center, heading, set_facecolor=True, set_edges=False):

        hr = np.deg2rad(heading)
        x_rr = x_center - self._d * np.cos(self._alpha + hr)
        y_rr = y_center - self._d * np.sin(self._alpha + hr)

        self.rectangle_patch.set_xy((x_rr, y_rr))  # this is the left-bottom point of the Rectangle-Patch
        self.rectangle_patch.angle = heading

        if set_facecolor:
            self.rectangle_patch.set_alpha(1.0)
        else:
            if set_edges:
                self.rectangle_patch.set_alpha(1.0)
                self.rectangle_patch.set_facecolor("none")
                self.rectangle_patch.set_edgecolor(self.color)
            else:
                self.rectangle_patch.set_alpha(0.2)

        self.id_text.set_position([x_center + 3, y_center + 3])

    def set_uncertainty_ellipse(self):
        self.uncertainty_ellipse_68 = UncertaintyEllipse(self.color)
        self.ax.add_patch(self.uncertainty_ellipse_68.e)
        self.uncertainty_ellipse_95 = UncertaintyEllipse(self.color)
        self.ax.add_patch(self.uncertainty_ellipse_95.e)
        self.uncertainty_ellipse_99 = UncertaintyEllipse(self.color)
        self.ax.add_patch(self.uncertainty_ellipse_99.e)
        self.uncertainty_ellipses = [
            self.uncertainty_ellipse_68,
            self.uncertainty_ellipse_95,
            self.uncertainty_ellipse_99,
        ]

    def update_uncertainty_ellipse(self, x, y, heading, uncertainty_ellipses):
        for i in range(int(len(uncertainty_ellipses) / 2)):
            ellipse_inner_width, ellipse_inner_height = uncertainty_ellipses[2 * i : 2 * (i + 1)]
            self.uncertainty_ellipses[i].update_transformation(x, y, heading)
            self.uncertainty_ellipses[i].update_uncertainty(ellipse_inner_width, ellipse_inner_height)

    def set_visible_area(self):
        """Define the patch of the sensor scan area"""
        pass

    def update_visible_area(self, visible_regions):
        """Define the patch of the sensor scan area"""

        if self.visible_area_patch is not None:
            self.visible_area_patch.remove()

        patches = []
        if isinstance(visible_regions, (list, np.ndarray)):
            for v in visible_regions:
                if type(v) is np.ndarray:
                    patches.append(Polygon(v))
                elif type(v) is Polygon:
                    patches.append(v)
                else:
                    raise Exception("Undefined type for visible area")
            visible_regions = PatchCollection(patches)
        elif type(visible_regions) is PatchCollection:
            pass
        else:
            raise Exception("Undefined type for visible area")

        visible_regions.set_alpha(0.4)  # hex(0.4*255) = 66
        visible_regions.set_facecolor(self.color)
        visible_regions.set_linewidth(0)

        self.visible_area_patch = visible_regions
        self.ax.add_collection(self.visible_area_patch)

    def set_stop_pos(self):
        self.ax.lines_line2d_stop_pos = self.ax.plot([], [], "*", color=self.color, markersize=6)

    def update_stop_pos(self, stop_position):
        x, y = stop_position
        self.ax.lines_line2d_stop_pos.set_data(x, y)

    def center_vehicle_in_plot(self, x, y, zoom):
        self.ax.set_xlim(x - zoom, x + zoom)
        self.ax.set_ylim(y - zoom, y + zoom)
